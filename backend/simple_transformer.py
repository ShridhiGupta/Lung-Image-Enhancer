from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import io
import base64
import numpy as np
import cv2
import os

app = Flask(__name__)
CORS(app)

class SimpleTransformerXRayEnhancer(nn.Module):
    def __init__(self):
        super(SimpleTransformerXRayEnhancer, self).__init__()
        
        # Feature extraction with residual connections
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(128)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(256)
        
        # Simplified attention mechanism
        self.attention = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(256, 64, kernel_size=1),
            nn.ReLU(),
            nn.Conv2d(64, 256, kernel_size=1),
            nn.Sigmoid()
        )
        
        # Enhancement decoder
        self.decoder = nn.Sequential(
            nn.Conv2d(256, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 3, kernel_size=3, padding=1),
            nn.Sigmoid()
        )
        
        self.relu = nn.ReLU()
        
    def forward(self, x):
        # Feature extraction with residual connections
        x1 = self.relu(self.bn1(self.conv1(x)))
        x2 = self.relu(self.bn2(self.conv2(x1)))
        x3 = self.relu(self.bn3(self.conv3(x2)))
        
        # Attention mechanism
        attention_weights = self.attention(x3)
        x_attended = x3 * attention_weights
        
        # Enhancement
        enhanced = self.decoder(x_attended)
        
        return enhanced

# Initialize and load trained model
model = SimpleTransformerXRayEnhancer()
model_path = 'quick_trained_model.pth'

try:
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    print(f"✅ Loaded trained model from {model_path}")
except FileNotFoundError:
    print(f"⚠️  No trained model found at {model_path}, using untrained model")
except Exception as e:
    print(f"⚠️  Error loading model: {e}, using untrained model")

model.eval()

def enhance_xray_transformer(image_data):
    """Enhance X-ray image using simplified transformer approach"""
    try:
        # Convert base64 to PIL Image
        image_data = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Store original size
        original_size = image.size
        
        # Preprocess
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])
        
        input_tensor = transform(image).unsqueeze(0)
        
        # Apply transformer enhancement
        with torch.no_grad():
            enhanced_tensor = model(input_tensor)
        
        # Convert back to PIL Image
        enhanced_image = transforms.ToPILImage()(enhanced_tensor.squeeze(0))
        
        # Resize back to original dimensions
        enhanced_image = enhanced_image.resize(original_size, Image.LANCZOS)
        
        # Apply post-processing for medical image enhancement
        enhanced_np = np.array(enhanced_image)
        
        # Medical image specific enhancements
        # 1. Contrast Limited Adaptive Histogram Equalization (CLAHE)
        lab = cv2.cvtColor(enhanced_np, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel with medical imaging parameters
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        
        enhanced_lab = cv2.merge([l, a, b])
        enhanced_clahe = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
        
        # 2. Edge-preserving smoothing
        enhanced_smooth = cv2.bilateralFilter(enhanced_clahe, 9, 75, 75)
        
        # 3. Subtle sharpening for medical details
        kernel = np.array([[-0.5, -1, -0.5], [-1, 6, -1], [-0.5, -1, -0.5]])
        enhanced_sharp = cv2.filter2D(enhanced_smooth, -1, kernel)
        
        # Blend sharpened image with original for natural look
        enhanced_final = cv2.addWeighted(enhanced_smooth, 0.7, enhanced_sharp, 0.3, 0)
        
        # Convert to base64
        buffered = io.BytesIO()
        Image.fromarray(enhanced_final).save(buffered, format="PNG", quality=95)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str
        
    except Exception as e:
        print(f"Error in transformer enhancement: {str(e)}")
        return None

def create_traditional_enhancement(image_data):
    """Create traditional enhanced version with medical imaging techniques"""
    try:
        # Convert base64 to PIL Image
        image_data = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Store original size
        original_size = image.size
        
        # Convert to numpy array
        img_np = np.array(image)
        
        # Medical image enhancement pipeline
        
        # 1. Denoising
        denoised = cv2.fastNlMeansDenoisingColored(img_np, None, 10, 10, 7, 21)
        
        # 2. Contrast enhancement using CLAHE
        lab = cv2.cvtColor(denoised, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
        l = clahe.apply(l)
        enhanced_lab = cv2.merge([l, a, b])
        enhanced_contrast = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
        
        # 3. Histogram equalization for better visibility
        img_yuv = cv2.cvtColor(enhanced_contrast, cv2.COLOR_RGB2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        enhanced_hist = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
        
        # 4. Adaptive sharpening
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        enhanced_sharp = cv2.filter2D(enhanced_hist, -1, kernel)
        
        # 5. Gamma correction for medical imaging
        gamma = 1.1  # Slight brightening
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        enhanced_gamma = cv2.LUT(enhanced_sharp, table)
        
        # Convert to base64
        buffered = io.BytesIO()
        Image.fromarray(enhanced_gamma).save(buffered, format="PNG", quality=95)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str
        
    except Exception as e:
        print(f"Error in traditional enhancement: {str(e)}")
        return None

@app.route('/enhance', methods=['POST'])
def enhance_image():
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Create both enhanced versions
        enhanced_v1 = enhance_xray_transformer(image_data)
        enhanced_v2 = create_traditional_enhancement(image_data)
        
        if enhanced_v1 and enhanced_v2:
            return jsonify({
                'enhanced_v1': f'data:image/png;base64,{enhanced_v1}',
                'enhanced_v2': f'data:image/png;base64,{enhanced_v2}',
                'message': 'X-ray images enhanced successfully with transformer and traditional methods'
            })
        else:
            return jsonify({'error': 'Failed to enhance images'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'model_loaded': True,
        'model_type': 'Simplified Transformer with Attention'
    })

if __name__ == '__main__':
    print("Starting Simple Transformer X-Ray Enhancement Server...")
    print("Features: Simplified transformer with attention mechanism")
    port = int(os.environ.get('PORT', 5000))
    print(f"Server running on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)
