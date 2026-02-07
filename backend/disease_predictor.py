import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2
import io
import base64

class LungDiseasePredictor(nn.Module):
    def __init__(self, num_classes=5):
        super(LungDiseasePredictor, self).__init__()
        
        # Feature extraction layers
        self.features = nn.Sequential(
            # First block
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Second block
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Third block
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Fourth block
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((7, 7))
        )
        
        # Classification layers
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 7 * 7, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, num_classes)
        )
        
    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

class DiseasePredictionService:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = LungDiseasePredictor().to(self.device)
        self.model.eval()
        
        # Class labels
        self.classes = [
            'Normal',
            'Bacterial Pneumonia', 
            'Viral Pneumonia',
            'Tuberculosis',
            'Corona Virus Disease'
        ]
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        # Load trained weights if available
        self.load_model()
    
    def load_model(self):
        try:
            model_path = 'disease_model.pth'
            checkpoint = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            print(f"✅ Disease prediction model loaded from {model_path}")
        except FileNotFoundError:
            print(f"⚠️  No trained disease model found, using untrained model")
        except Exception as e:
            print(f"⚠️  Error loading disease model: {e}")
    
    def predict_disease(self, image_base64):
        """
        Predict disease from base64 image
        Returns: dict with predictions and confidence scores
        """
        try:
            # Decode base64 image
            image_data = base64.b64decode(image_base64.split(',')[1])
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            
            # Preprocess image
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence_scores = probabilities.cpu().numpy()[0]
                
            # Create predictions dict
            predictions = []
            for i, (class_name, confidence) in enumerate(zip(self.classes, confidence_scores)):
                predictions.append({
                    'disease': class_name,
                    'confidence': float(confidence),
                    'percentage': f"{confidence * 100:.2f}%"
                })
            
            # Sort by confidence
            predictions.sort(key=lambda x: x['confidence'], reverse=True)
            
            # Get top prediction
            top_prediction = predictions[0]
            
            # Generate medical report
            report = self.generate_medical_report(predictions)
            
            return {
                'success': True,
                'predictions': predictions,
                'top_prediction': top_prediction,
                'report': report,
                'confidence_threshold': top_prediction['confidence'] > 0.5
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'predictions': [],
                'top_prediction': None,
                'report': None
            }
    
    def generate_medical_report(self, predictions):
        """Generate a medical report based on predictions"""
        top_pred = predictions[0]
        confidence = top_pred['confidence']
        disease = top_pred['disease']
        
        if confidence > 0.8:
            severity = "High Confidence"
            recommendation = "Immediate medical consultation recommended"
        elif confidence > 0.6:
            severity = "Moderate Confidence"
            recommendation = "Medical consultation advised"
        elif confidence > 0.4:
            severity = "Low Confidence"
            recommendation = "Further diagnostic tests recommended"
        else:
            severity = "Very Low Confidence"
            recommendation = "Consultation with specialist recommended"
        
        # Disease-specific information
        disease_info = {
            'Normal': {
                'description': 'No apparent abnormalities detected in the lung X-ray.',
                'follow_up': 'Routine check-up if no symptoms present.'
            },
            'Bacterial Pneumonia': {
                'description': 'Signs of bacterial infection in lung tissue.',
                'follow_up': 'Antibiotic therapy and close monitoring.'
            },
            'Viral Pneumonia': {
                'description': 'Patterns suggesting viral lung infection.',
                'follow_up': 'Antiviral treatment and supportive care.'
            },
            'Tuberculosis': {
                'description': 'Indicators of tuberculosis infection.',
                'follow_up': 'Anti-TB medication regimen and contact tracing.'
            },
            'Corona Virus Disease': {
                'description': 'COVID-19 related lung changes.',
                'follow_up': 'Isolation, monitoring, and appropriate COVID treatment.'
            }
        }
        
        info = disease_info.get(disease, disease_info['Normal'])
        
        report = f"""
MEDICAL ANALYSIS REPORT
======================

Primary Finding: {disease}
Confidence Level: {confidence * 100:.1f}%
Assessment Severity: {severity}

Description:
{info['description']}

Recommendations:
{recommendation}
{info['follow_up']}

All Predictions:
"""
        for pred in predictions:
            report += f"- {pred['disease']}: {pred['percentage']}\n"
        
        report += f"""
Note: This is an AI-assisted analysis and should be reviewed by a qualified healthcare professional.
Always consult with a medical doctor for definitive diagnosis and treatment.
"""
        
        return report.strip()

# Create global instance
disease_service = DiseasePredictionService()
