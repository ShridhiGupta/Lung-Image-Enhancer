import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from enhanced_app import TransformerXRayEnhancer
import os

class SimpleXRayDataset(Dataset):
    def __init__(self, num_samples=200, transform=None):
        self.transform = transform
        self.num_samples = num_samples
        np.random.seed(42)
        
    def __len__(self):
        return self.num_samples
    
    def __getitem__(self, idx):
        # Create synthetic X-ray-like image with medical characteristics
        base_img = np.zeros((224, 224, 3), dtype=np.uint8)
        
        # Add lung-like structures
        center_y, center_x = 112, 112
        
        # Left lung
        for i in range(80, 140):
            for j in range(40, 100):
                if np.sqrt((i-center_y)**2 + (j-center_x+30)**2) < 40:
                    base_img[i, j] = [180 + np.random.randint(-20, 20)] * 3
        
        # Right lung
        for i in range(80, 140):
            for j in range(140, 200):
                if np.sqrt((i-center_y)**2 + (j-center_x-30)**2) < 40:
                    base_img[i, j] = [180 + np.random.randint(-20, 20)] * 3
        
        # Add heart shadow
        for i in range(90, 130):
            for j in range(100, 140):
                if np.sqrt((i-center_y)**2 + (j-center_x)**2) < 20:
                    base_img[i, j] = [160 + np.random.randint(-15, 15)] * 3
        
        # Add noise and artifacts
        noise = np.random.normal(0, 10, (224, 224, 3))
        base_img = np.clip(base_img + noise, 0, 255).astype(np.uint8)
        
        # Convert to PIL Image
        image = Image.fromarray(base_img)
        
        if self.transform:
            image = self.transform(image)
        
        # Create enhanced target
        # Apply enhancement directly to the numpy array before converting to tensor
        enhanced_np = np.clip(base_img.astype(np.float32) * 1.2 + 20, 0, 255).astype(np.uint8)
        target = transforms.ToTensor()(Image.fromarray(enhanced_np))
        
        return image, target

def train_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Training on device: {device}")
    
    # Initialize model
    model = TransformerXRayEnhancer()
    model.to(device)
    
    # Loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)
    
    # Data loading
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    
    train_dataset = SimpleXRayDataset(num_samples=150, transform=transform)
    val_dataset = SimpleXRayDataset(num_samples=50, transform=transform)
    
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False)
    
    # Training loop
    num_epochs = 40
    train_losses = []
    val_losses = []
    best_val_loss = float('inf')
    
    print("Starting Training...")
    print(f"Target: {num_epochs} epochs, Loss < 0.9")
    
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        
        for i, (inputs, targets) in enumerate(train_loader):
            inputs, targets = inputs.to(device), targets.to(device)
            
            optimizer.zero_grad()
            
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            
            running_loss += loss.item()
        
        # Validation
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for inputs, targets in val_loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                val_loss += loss.item()
        
        epoch_train_loss = running_loss / len(train_loader)
        epoch_val_loss = val_loss / len(val_loader)
        
        train_losses.append(epoch_train_loss)
        val_losses.append(epoch_val_loss)
        
        scheduler.step(epoch_val_loss)
        
        print(f'Epoch [{epoch+1}/{num_epochs}]')
        print(f'  Train Loss: {epoch_train_loss:.4f}')
        print(f'  Val Loss: {epoch_val_loss:.4f}')
        
        if epoch_val_loss < best_val_loss:
            best_val_loss = epoch_val_loss
            torch.save(model.state_dict(), 'best_model.pth')
            print(f'  New best model! Val Loss: {epoch_val_loss:.4f}')
        
        if epoch_val_loss < 0.9:
            print(f'  🎯 Target achieved! Loss < 0.9')
        
        print('-' * 40)
    
    # Save final model
    torch.save(model.state_dict(), 'final_model.pth')
    
    # Plot results
    plt.figure(figsize=(10, 5))
    plt.plot(train_losses, label='Training Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.axhline(y=0.9, color='red', linestyle='--', label='Target (< 0.9)')
    plt.title('Training Progress')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig('training_results.png')
    plt.show()
    
    print(f"\n🎉 Training Completed!")
    print(f"Final Validation Loss: {val_losses[-1]:.4f}")
    print(f"Best Validation Loss: {best_val_loss:.4f}")
    print(f"Target Achieved: {'✅ Yes' if best_val_loss < 0.9 else '❌ No'}")
    
    return model, train_losses, val_losses

if __name__ == '__main__':
    model, train_losses, val_losses = train_model()
