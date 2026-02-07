import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
import numpy as np
import os
from app import XRayEnhancer
import matplotlib.pyplot as plt

class XRayDataset(Dataset):
    def __init__(self, transform=None):
        self.transform = transform
        # For demo purposes, we'll create synthetic data
        # In real usage, you would load actual X-ray images here
        
    def __len__(self):
        return 100  # Synthetic dataset size
    
    def __getitem__(self, idx):
        # Create synthetic X-ray-like image
        img = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
        img = Image.fromarray(img)
        
        if self.transform:
            img = self.transform(img)
        
        # Target is a slightly enhanced version
        target = transforms.functional.adjust_brightness(img, 1.2)
        target = transforms.functional.adjust_contrast(target, 1.1)
        
        return img, target

def train_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Initialize model
    model = XRayEnhancer()
    model.to(device)
    
    # Loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Data loading
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    
    dataset = XRayDataset(transform=transform)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)
    
    # Training loop
    num_epochs = 40  # More than 35 as requested
    losses = []
    
    print("Starting training...")
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        
        for i, (inputs, targets) in enumerate(dataloader):
            inputs, targets = inputs.to(device), targets.to(device)
            
            # Zero the parameter gradients
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            
            # Backward pass and optimize
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
        
        epoch_loss = running_loss / len(dataloader)
        losses.append(epoch_loss)
        
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}')
        
        # Save checkpoint
        if (epoch + 1) % 10 == 0:
            torch.save(model.state_dict(), f'model_checkpoint_epoch_{epoch+1}.pth')
    
    # Save final model
    torch.save(model.state_dict(), 'xray_enhancer_final.pth')
    
    # Plot training loss
    plt.figure(figsize=(10, 5))
    plt.plot(losses)
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.grid(True)
    plt.savefig('training_loss.png')
    plt.show()
    
    print(f"Training completed. Final loss: {losses[-1]:.4f}")
    print(f"Model saved as 'xray_enhancer_final.pth'")

if __name__ == '__main__':
    train_model()
