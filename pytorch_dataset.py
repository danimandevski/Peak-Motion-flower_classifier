import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split
import torch.nn as nn
import torch.optim as optim
from torchvision import models
import tqdm
from PIL import Image
import os

from torchvision.models import vgg19, VGG19_BN_Weights


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

data_dir = "inat_images"  # Folder containing species subfolders

# Image augmentation
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(), 
    transforms.RandomRotation(30),     
    transforms.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5),
    transforms.ToTensor(),  
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # ImageNet normalization
])

test_transform = transforms.Compose([
    transforms.Resize((224, 224)),  
    transforms.ToTensor(),  
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def remove_corrupt_images():
    for species in os.listdir(data_dir):
        species_path = os.path.join(data_dir, species)
        
        if os.path.isdir(species_path): 
            for img_file in os.listdir(species_path):
                img_path = os.path.join(species_path, img_file)
                try:
                    with Image.open(img_path) as img:
                        img.verify()  # Check if the image is valid
                except (IOError, Image.UnidentifiedImageError):
                    print(f"Removing corrupt image: {img_path}")
                    os.remove(img_path)  # Delete corrupt image

def get_data():
    dataset = datasets.ImageFolder(root=data_dir, transform=train_transform) # ImageFolder (auto-labels folders)

    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

    # Check dataset info
    print(f"Total images: {len(dataset)}")
    print(f"Train images: {len(train_dataset)} | Test images: {len(test_dataset)}")
    print(f"Classes: {dataset.classes}")  

    # Apply test transforms to test dataset
    test_dataset.dataset.transform = test_transform  

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=4)
    
    return train_loader, test_loader

def evaluate(model, test_loader):
    model.eval()  
    correct, total = 0, 0

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)

    test_acc = 100 * correct / total
    print(f"Test Accuracy: {test_acc:.2f}%\n")

def train(model, train_loader, test_loader, optimizer, criterion, epochs=10):
    total_step = len(train_loader)
    
    for epoch in range(epochs):
        progress_bar = tqdm.tqdm(total=total_step, desc=f'Epoch {epoch + 1}')

        model.train()  
        running_loss = 0.0
        correct, total = 0, 0

        for idx, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)
            
            progress_bar.n = idx + 1
            progress_bar.refresh()
        
        train_acc = 100 * correct / total
        print(f"Epoch {epoch+1}/{epochs} - Loss: {running_loss/len(train_loader):.4f} - Train Acc: {train_acc:.2f}%")

        evaluate(model, test_loader)

def main():
    remove_corrupt_images()

    model = vgg19(weights = VGG19_BN_Weights)  

    # Modify the classifier for 5 species
    num_features = model.classifier[-1].in_features  # Get input size of last FC layer
    model.classifier[-1] = nn.Linear(num_features, 5)  # Change output layer to 5 classes

    # Move model to GPU if available
    model = model.to(device)

    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001)

    train_loader, test_loader = get_data()
    train(model, train_loader, test_loader, optimizer, criterion, epochs=10)
    
    torch.save(model, 'plant_classifier')


if __name__ == '__main__':
    main()