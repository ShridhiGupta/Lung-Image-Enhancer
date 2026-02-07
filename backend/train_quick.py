import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import numpy as np
import cv2
from pathlib import Path

class SimpleXRayDataset(Dataset):
    def __init__(self, num_samples=100):
        self.num_samples = num_samples
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])
    
    def __len__(self):
        return self.num_samples
    
    def __getitem__(self, idx):
        # Generate synthetic X-ray like images
        # Create a grayscale medical image pattern
        img = np.random.randint(50, 200, (224, 224, 3), dtype=np.uint8)
        
        # Add some medical-like structures
        center = (112, 112)
        cv2.circle(img, center, 60, (150, 150, 150), -1)  # Lung area
        cv2.circle(img, center, 30, (100, 100, 100), -1)  # Heart area
        
        # Add noise
        noise = np.random.normal(0, 10, img.shape).astype(np.uint8)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        # Convert to PIL
        image = Image.fromarray(img)
        
        # Create enhanced target
        enhanced = self.create_enhanced_target(img)
        
        # Apply transforms
        if self.transform:
            image = self.transform(image)
        
        return image, enhanced
    
    def create_enhanced_target(self, img):
        # Apply CLAHE enhancement
        lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        enhanced_lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)
        
        # Convert to tensor
        enhanced_tensor = torch.from_numpy(enhanced).float() / 255.0
        enhanced_tensor = enhanced_tensor.permute(2, 0, 1)
        
        return enhanced_tensor

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

def train_model():
    print("🏥 Quick Training Medical X-Ray Enhancement Model")
    print("=" * 50)
    
    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🖥️  Using device: {device}")
    
    # Create dataset
    dataset = SimpleXRayDataset(num_samples=200)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True)
    
    # Model
    model = SimpleTransformerXRayEnhancer().to(device)
    print(f"🧠 Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Loss and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Quick training loop
    num_epochs = 10  # Quick training
    print(f"\n🚀 Starting quick training for {num_epochs} epochs...")
    
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0.0
        
        for batch_idx, (images, targets) in enumerate(dataloader):
            images, targets = images.to(device), targets.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch+1}/{num_epochs}: Loss: {avg_loss:.4f}")
        
        # Early stopping if loss is good enough
        if avg_loss < 0.5:
            print(f"🎉 Good enough loss achieved: {avg_loss:.4f}")
            break
    
    # Save model
    torch.save(model.state_dict(), 'quick_trained_model.pth')
    print(f"💾 Model saved as 'quick_trained_model.pth'")
    
    return model

if __name__ == "__main__":
    model = train_model()
    print("🎉 Quick training completed!")
