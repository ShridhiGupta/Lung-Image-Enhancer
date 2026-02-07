import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import cv2
from tqdm import tqdm

class LungXRayDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
        
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        # Load image
        image_path = self.image_paths[idx]
        image = Image.open(image_path).convert('RGB')
        
        # Apply transforms
        if self.transform:
            image = self.transform(image)
        
        # Create enhanced target using traditional methods
        enhanced_image = self.create_enhanced_target(image)
        
        return image, enhanced_image
    
    def create_enhanced_target(self, image):
        # Convert to numpy for OpenCV processing
        img_np = image.permute(1, 2, 0).numpy()
        img_np = (img_np * 255).astype(np.uint8)
        
        # Convert to grayscale for medical processing
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Apply median filter for noise reduction
        enhanced = cv2.medianBlur(enhanced, 3)
        
        # Convert back to 3 channels
        enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
        
        # Convert back to tensor
        enhanced_tensor = torch.from_numpy(enhanced_rgb).float() / 255.0
        enhanced_tensor = enhanced_tensor.permute(2, 0, 1)
        
        return enhanced_tensor

class EfficientMedicalXRayEnhancer(nn.Module):
    def __init__(self):
        super(EfficientMedicalXRayEnhancer, self).__init__()
        
        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # 128x128
            
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # 64x64
            
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # 32x32
        )
        
        # Lightweight attention mechanism
        self.channel_attention = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(128, 32, 1),
            nn.ReLU(),
            nn.Conv2d(32, 128, 1),
            nn.Sigmoid()
        )
        
        # Decoder
        self.decoder = nn.Sequential(
            nn.Conv2d(128, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),  # 64x64
            
            nn.Conv2d(64, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),  # 128x128
            
            nn.Conv2d(32, 16, 3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),  # 256x256
            
            nn.Conv2d(16, 8, 3, padding=1),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True),
            
            nn.Conv2d(8, 3, 3, padding=1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        # Encode
        encoded = self.encoder(x)
        
        # Apply channel attention
        attention_weights = self.channel_attention(encoded)
        attended = encoded * attention_weights
        
        # Decode
        enhanced = self.decoder(attended)
        
        return enhanced

def load_dataset(dataset_path, max_samples=None):
    print("📊 Loading medical X-ray dataset...")
    
    dataset_path = Path(dataset_path)
    image_paths = []
    labels = []
    
    categories = ["normal", "bacterial_pneumonia", "viral_pneumonia", "tuberculosis", "corona_virus"]
    
    for category_idx, category in enumerate(categories):
        category_path = dataset_path / category
        if category_path.exists():
            for img_path in category_path.glob("*.jpg"):
                image_paths.append(str(img_path))
                labels.append(category_idx)
            for img_path in category_path.glob("*.png"):
                image_paths.append(str(img_path))
                labels.append(category_idx)
    
    print(f"✅ Found {len(image_paths)} images across {len(categories)} categories")
    
    # Limit samples for memory efficiency
    if max_samples and len(image_paths) > max_samples:
        indices = np.random.choice(len(image_paths), max_samples, replace=False)
        image_paths = [image_paths[i] for i in indices]
        labels = [labels[i] for i in indices]
        print(f"📊 Limited to {len(image_paths)} samples for memory efficiency")
    
    # Split dataset
    train_paths, val_paths, train_labels, val_labels = train_test_split(
        image_paths, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    return (train_paths, train_labels), (val_paths, val_labels)

def train_model():
    print("🏥 Training Efficient Medical X-Ray Enhancement Model")
    print("=" * 60)
    
    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🖥️  Using device: {device}")
    
    # Dataset path
    dataset_path = Path(__file__).parent.parent / "dataset" / "lungs_disease"
    
    # Load dataset (limited for memory efficiency)
    (train_paths, train_labels), (val_paths, val_labels) = load_dataset(dataset_path, max_samples=1000)
    
    # Transforms
    transform = transforms.Compose([
        transforms.Resize((128, 128)),  # Smaller size for memory efficiency
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Create datasets
    train_dataset = LungXRayDataset(train_paths, train_labels, transform)
    val_dataset = LungXRayDataset(val_paths, val_labels, transform)
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True, num_workers=0)  # Reduced batch size
    val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False, num_workers=0)
    
    print(f"📚 Training samples: {len(train_dataset)}")
    print(f"📚 Validation samples: {len(val_dataset)}")
    
    # Model
    model = EfficientMedicalXRayEnhancer().to(device)
    print(f"🧠 Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Loss and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=3, factor=0.5)
    
    # Training loop
    num_epochs = 40
    train_losses = []
    val_losses = []
    best_val_loss = float('inf')
    
    print(f"\n🚀 Starting training for {num_epochs} epochs...")
    
    for epoch in range(num_epochs):
        # Training
        model.train()
        train_loss = 0.0
        
        train_pbar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs} [Train]")
        for batch_idx, (images, targets) in enumerate(train_pbar):
            images, targets = images.to(device), targets.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            train_pbar.set_postfix({'loss': f'{loss.item():.4f}'})
        
        avg_train_loss = train_loss / len(train_loader)
        train_losses.append(avg_train_loss)
        
        # Validation
        model.eval()
        val_loss = 0.0
        
        with torch.no_grad():
            val_pbar = tqdm(val_loader, desc=f"Epoch {epoch+1}/{num_epochs} [Val]")
            for images, targets in val_pbar:
                images, targets = images.to(device), targets.to(device)
                outputs = model(images)
                loss = criterion(outputs, targets)
                val_loss += loss.item()
                val_pbar.set_postfix({'loss': f'{loss.item():.4f}'})
        
        avg_val_loss = val_loss / len(val_loader)
        val_losses.append(avg_val_loss)
        
        # Learning rate scheduling
        scheduler.step(avg_val_loss)
        
        # Save best model
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), 'best_medical_enhancer.pth')
            print(f"💾 New best model saved (val_loss: {avg_val_loss:.4f})")
        
        print(f"Epoch {epoch+1}/{num_epochs}: Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}")
        
        # Check if target loss achieved
        if avg_val_loss < 0.9:
            print(f"🎉 Target loss < 0.9 achieved! (val_loss: {avg_val_loss:.4f})")
            break
    
    # Save final model
    torch.save(model.state_dict(), 'final_medical_enhancer.pth')
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(train_losses, label='Training Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training History')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(val_losses, label='Validation Loss', color='orange')
    plt.axhline(y=0.9, color='r', linestyle='--', label='Target Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Validation Loss')
    plt.title('Validation Loss Progress')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.show()
    
    print(f"\n🎉 Training completed!")
    print(f"📊 Best validation loss: {best_val_loss:.4f}")
    print(f"💾 Models saved: best_medical_enhancer.pth, final_medical_enhancer.pth")
    print(f"📈 Training plot saved: training_history.png")
    
    return model

if __name__ == "__main__":
    model = train_model()
