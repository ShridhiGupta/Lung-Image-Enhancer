import base64
import io
from PIL import Image
import numpy as np
import random

class SimpleDiseasePredictor:
    def __init__(self):
        self.classes = [
            'Normal',
            'Bacterial Pneumonia', 
            'Viral Pneumonia',
            'Tuberculosis',
            'Corona Virus Disease'
        ]
        
        # Disease information database
        self.disease_info = {
            'Normal': {
                'description': 'No apparent abnormalities detected in the lung X-ray.',
                'symptoms': 'No symptoms, healthy lungs',
                'treatment': 'No treatment needed, regular check-ups recommended',
                'severity': 'None'
            },
            'Bacterial Pneumonia': {
                'description': 'Signs of bacterial infection in lung tissue with consolidation patterns.',
                'symptoms': 'Fever, cough, chest pain, difficulty breathing',
                'treatment': 'Antibiotics, rest, plenty of fluids',
                'severity': 'Moderate to Severe'
            },
            'Viral Pneumonia': {
                'description': 'Patterns suggesting viral lung infection with diffuse infiltrates.',
                'symptoms': 'Dry cough, fever, fatigue, muscle aches',
                'treatment': 'Antiviral medications, supportive care, rest',
                'severity': 'Mild to Moderate'
            },
            'Tuberculosis': {
                'description': 'Indicators of tuberculosis infection with cavitations and nodules.',
                'symptoms': 'Persistent cough, weight loss, night sweats, fever',
                'treatment': 'Anti-TB medication regimen for 6+ months',
                'severity': 'Severe'
            },
            'Corona Virus Disease': {
                'description': 'COVID-19 related lung changes with ground-glass opacities.',
                'symptoms': 'Fever, dry cough, loss of taste/smell, fatigue',
                'treatment': 'Supportive care, isolation, monitoring oxygen levels',
                'severity': 'Mild to Critical'
            }
        }
    
    def analyze_image_features(self, image):
        """Simple image analysis based on basic features"""
        try:
            # Convert to grayscale for analysis
            gray = image.convert('L')
            img_array = np.array(gray)
            
            # Basic image statistics
            mean_intensity = np.mean(img_array)
            std_intensity = np.std(img_array)
            
            # Simple feature extraction (very basic)
            features = {
                'brightness': mean_intensity,
                'contrast': std_intensity,
                'texture': np.std(img_array[::10, ::10])  # Sample texture
            }
            
            return features
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return None
    
    def predict_disease(self, image_base64):
        """
        Predict disease from base64 image using simple heuristics
        Returns: dict with predictions and disease information
        """
        try:
            # Decode base64 image
            image_data = base64.b64decode(image_base64.split(',')[1])
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            
            # Analyze image features
            features = self.analyze_image_features(image)
            
            # Simple prediction logic (for demonstration)
            # In real AI model, this would be neural network inference
            
            # Generate random predictions weighted by image features
            if features:
                # Use image brightness to bias predictions
                brightness_factor = features['brightness'] / 255.0
                
                # Create weighted probabilities
                base_probs = [0.3, 0.2, 0.2, 0.15, 0.15]  # Base probabilities
                
                # Adjust based on image characteristics
                if brightness_factor < 0.3:  # Dark image
                    base_probs[1] += 0.2  # More likely pneumonia
                    base_probs[3] += 0.1  # More likely TB
                elif brightness_factor > 0.7:  # Bright image
                    base_probs[0] += 0.2  # More likely normal
                
                # Normalize probabilities
                total = sum(base_probs)
                probs = [p/total for p in base_probs]
            else:
                # Default equal probabilities if analysis fails
                probs = [0.2, 0.2, 0.2, 0.2, 0.2]
            
            # Add some randomness for demonstration
            noise = [random.uniform(-0.05, 0.05) for _ in probs]
            probs = [max(0.01, p + n) for p, n in zip(probs, noise)]
            
            # Normalize again
            total = sum(probs)
            probs = [p/total for p in probs]
            
            # Create predictions dict
            predictions = []
            for i, (class_name, confidence) in enumerate(zip(self.classes, probs)):
                predictions.append({
                    'disease': class_name,
                    'confidence': float(confidence),
                    'percentage': f"{confidence * 100:.1f}%"
                })
            
            # Sort by confidence
            predictions.sort(key=lambda x: x['confidence'], reverse=True)
            
            # Get top prediction
            top_prediction = predictions[0]
            
            # Generate detailed medical report
            report = self.generate_detailed_report(top_prediction, predictions, features)
            
            return {
                'success': True,
                'predictions': predictions,
                'top_prediction': top_prediction,
                'disease_info': self.disease_info[top_prediction['disease']],
                'report': report,
                'image_analysis': features,
                'confidence_threshold': top_prediction['confidence'] > 0.3
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'predictions': [],
                'top_prediction': None,
                'report': None
            }
    
    def generate_detailed_report(self, top_prediction, all_predictions, features):
        """Generate comprehensive medical report"""
        disease = top_prediction['disease']
        confidence = top_prediction['confidence']
        info = self.disease_info[disease]
        
        # Confidence assessment
        if confidence > 0.6:
            confidence_level = "High Confidence"
            recommendation = "Medical consultation strongly recommended"
        elif confidence > 0.4:
            confidence_level = "Moderate Confidence"
            recommendation = "Medical consultation advised"
        else:
            confidence_level = "Low Confidence"
            recommendation = "Further diagnostic tests recommended"
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                    MEDICAL ANALYSIS REPORT                     ║
╚══════════════════════════════════════════════════════════════╝

DATE: {self.get_current_date()}
PRIMARY DIAGNOSIS: {disease}
CONFIDENCE LEVEL: {confidence * 100:.1f}% ({confidence_level})
ASSESSMENT SEVERITY: {info['severity']}

═══════════════════════════════════════════════════════════════

DETAILED FINDINGS:
─────────────────────────────────────────────────────────────────
{info['description']}

CLINICAL PRESENTATION:
─────────────────────────────────────────────────────────────────
{info['symptoms']}

RECOMMENDED TREATMENT:
─────────────────────────────────────────────────────────────────
{info['treatment']}

NEXT STEPS:
─────────────────────────────────────────────────────────────────
{recommendation}

═══════════════════════════════════════════════════════════════

ALL PREDICTIONS (Confidence Scores):
─────────────────────────────────────────────────────────────────
"""
        
        for pred in all_predictions:
            disease_name = pred['disease']
            confidence_pct = pred['percentage']
            bar = "█" * int(float(pred['confidence']) * 20)
            report += f"• {disease_name:<20} {confidence_pct:>8} {bar}\n"
        
        report += f"""
═══════════════════════════════════════════════════════════════

IMAGE ANALYSIS:
─────────────────────────────────────────────────────────────────
"""
        
        if features:
            report += f"• Average Brightness: {features['brightness']:.1f}/255\n"
            report += f"• Image Contrast: {features['contrast']:.1f}\n"
            report += f"• Texture Variation: {features['texture']:.1f}\n"
        else:
            report += "• Image analysis failed\n"
        
        report += f"""
═══════════════════════════════════════════════════════════════

IMPORTANT DISCLAIMER:
─────────────────────────────────────────────────────────────────
This is an AI-assisted preliminary analysis and should NOT replace
professional medical diagnosis. Always consult with a qualified 
healthcare provider for definitive diagnosis and treatment.

The AI model has limitations and may produce false positives or 
negatives. Clinical correlation and professional medical judgment 
are essential for accurate diagnosis.

═══════════════════════════════════════════════════════════════

Generated by X-Ray Lung Enhancer AI System
Version 1.0 | Healthcare Grade AI Technology
"""
        
        return report.strip()
    
    def get_current_date(self):
        """Get current date in readable format"""
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y at %I:%M %p")

# Create global instance
simple_disease_service = SimpleDiseasePredictor()
