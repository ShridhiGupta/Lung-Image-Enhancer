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

app = Flask(__name__)
CORS(app)

class SimpleXRayEnhancer(nn.Module):
    def __init__(self):
        super(SimpleXRayEnhancer, self).__init__()
        
        # Enhancement layers without transformer for faster startup
        self.enhance_conv = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 3, kernel_size=3, padding=1),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        # Enhancement through convolutional layers
        enhanced = self.enhance_conv(x)
        return enhanced

# Initialize the model
model = SimpleXRayEnhancer()
model.eval()

def enhance_xray_image_v1(image_data):
    """Enhance X-ray image using neural network approach"""
    try:
        # Convert base64 to PIL Image
        image_data = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Preprocess
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])
        
        input_tensor = transform(image).unsqueeze(0)
        
        # Apply enhancement
        with torch.no_grad():
            enhanced_tensor = model(input_tensor)
        
        # Convert back to PIL Image
        enhanced_image = transforms.ToPILImage()(enhanced_tensor.squeeze(0))
        
        # Apply additional image processing for better quality
        enhanced_np = np.array(enhanced_image)
        
        # Contrast enhancement
        lab = cv2.cvtColor(enhanced_np, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        l = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)).apply(l)
        enhanced_lab = cv2.merge([l, a, b])
        enhanced_contrast = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
        
        # Denoising
        enhanced_final = cv2.fastNlMeansDenoisingColored(enhanced_contrast, None, 10, 10, 7, 21)
        
        # Convert to base64
        buffered = io.BytesIO()
        Image.fromarray(enhanced_final).save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str
        
    except Exception as e:
        print(f"Error in enhancement: {str(e)}")
        return None

def create_alternative_enhancement(image_data):
    """Create alternative enhanced version with different processing"""
    try:
        # Convert base64 to PIL Image
        image_data = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Convert to numpy array
        img_np = np.array(image)
        
        # Apply different enhancement techniques
        # 1. Histogram equalization
        img_yuv = cv2.cvtColor(img_np, cv2.COLOR_RGB2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        enhanced_hist = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
        
        # 2. Sharpening
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        enhanced_sharp = cv2.filter2D(enhanced_hist, -1, kernel)
        
        # 3. Gamma correction
        gamma = 1.2
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        enhanced_gamma = cv2.LUT(enhanced_sharp, table)
        
        # Convert to base64
        buffered = io.BytesIO()
        Image.fromarray(enhanced_gamma).save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str
        
    except Exception as e:
        print(f"Error in alternative enhancement: {str(e)}")
        return None

@app.route('/enhance', methods=['POST'])
def enhance_image():
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Create both enhanced versions
        enhanced_v1 = enhance_xray_image_v1(image_data)
        enhanced_v2 = create_alternative_enhancement(image_data)
        
        if enhanced_v1 and enhanced_v2:
            return jsonify({
                'enhanced_v1': f'data:image/png;base64,{enhanced_v1}',
                'enhanced_v2': f'data:image/png;base64,{enhanced_v2}',
                'message': 'X-ray images enhanced successfully'
            })
        else:
            return jsonify({'error': 'Failed to enhance images'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': True})

if __name__ == '__main__':
    print("Starting X-Ray Enhancement Server...")
    print("Server running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
