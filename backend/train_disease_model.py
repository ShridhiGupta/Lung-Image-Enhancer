import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
import os
import numpy as np
from disease_predictor import LungDiseasePredictor
import matplotlib.pyplot as plt

class LungDiseaseDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.classes = ['Normal', 'Bacterial Pneumonia', 'Viral Pneumonia', 'Tuberculosis', 'Corona Virus Disease']
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.classes)}
        
        self.images = []
        self.labels = []
        
        # Load dataset
        self.load_dataset()
    
    def load_dataset(self):
        for class_name in self.classes:
            class_dir = os.path.join(self.root_dir, class_name)
            if os.path.exists(class_dir):
                for img_name in os.listdir(class_dir):
                    if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        img_path = os.path.join(class_dir, img_name)
                        self.images.append(img_path)
                        self.labels.append(self.class_to_idx[class_name])
        
        print(f"Loaded {len(self.images)} images from {len(self.classes)} classes")
        for class_name in self.classes:
            count = self.labels.count(self.class_to_idx[class_name])
            print(f"  {class_name}: {count} images")
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

def train_disease_model():
    print("🏥 Training Lung Disease Prediction Model")
    print("=" * 50)
    
    # Device setup
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Data transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                             std=[0.229, 0.224, 0.225])
    ])
    
    # Dataset paths
    dataset_path = '../dataset/lungs_disease'
    
    if not os.path.exists(dataset_path):
        print(f"⚠️  Dataset not found at {dataset_path}")
        print("Please run download_dataset.py and organize_dataset.py first")
        return
    
    # Create datasets
    try:
        full_dataset = LungDiseaseDataset(dataset_path, transform=transform)
        
        if len(full_dataset) == 0:
            print("⚠️  No images found in dataset")
            return
        
        # Split dataset
        train_size = int(0.8 * len(full_dataset))
        val_size = len(full_dataset) - train_size
        train_dataset, val_dataset = torch.utils.data.random_split(
            full_dataset, [train_size, val_size]
        )
        
        # Data loaders
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=2)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=2)
        
        print(f"Training samples: {len(train_dataset)}")
        print(f"Validation samples: {len(val_dataset)}")
        
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return
    
    # Model
    model = LungDiseasePredictor(num_classes=5).to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=3, factor=0.5)
    
    # Training loop
    num_epochs = 30
    train_losses = []
    val_losses = []
    train_accs = []
    val_accs = []
    
    print("\n🚀 Starting Training...")
    print("-" * 50)
    
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for batch_idx, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()
            
            if batch_idx % 10 == 0:
                print(f'Epoch [{epoch+1}/{num_epochs}], Batch [{batch_idx}/{len(train_loader)}], '
                      f'Loss: {loss.item():.4f}')
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
        
        # Calculate metrics
        train_loss_avg = train_loss / len(train_loader)
        val_loss_avg = val_loss / len(val_loader)
        train_acc = 100 * train_correct / train_total
        val_acc = 100 * val_correct / val_total
        
        train_losses.append(train_loss_avg)
        val_losses.append(val_loss_avg)
        train_accs.append(train_acc)
        val_accs.append(val_acc)
        
        # Learning rate scheduling
        scheduler.step(val_loss_avg)
        
        print(f'\nEpoch [{epoch+1}/{num_epochs}] Summary:')
        print(f'  Train Loss: {train_loss_avg:.4f}, Train Acc: {train_acc:.2f}%')
        print(f'  Val Loss: {val_loss_avg:.4f}, Val Acc: {val_acc:.2f}%')
        print(f'  Learning Rate: {optimizer.param_groups[0]["lr"]:.6f}')
        print('-' * 50)
        
        # Save best model
        if epoch == 0 or val_loss_avg < min(val_losses[:-1]):
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_loss_avg,
                'val_acc': val_acc,
                'train_losses': train_losses,
                'val_losses': val_losses,
                'train_accs': train_accs,
                'val_accs': val_accs
            }, 'disease_model.pth')
            print(f'✅ New best model saved at epoch {epoch+1}')
    
    print("\n🎉 Training Completed!")
    print(f"Best Validation Loss: {min(val_losses):.4f}")
    print(f"Best Validation Accuracy: {max(val_accs):.2f}%")
    
    # Plot training curves
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(train_accs, label='Train Accuracy')
    plt.plot(val_accs, label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('disease_model_training.png')
    plt.show()
    
    print("📊 Training curves saved as 'disease_model_training.png'")
    print("💾 Model saved as 'disease_model.pth'")

if __name__ == "__main__":
    train_disease_model()
