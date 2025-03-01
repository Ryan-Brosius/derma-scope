import torch
import torch.nn as nn
import torch.optim as optim
import medmnist
from medmnist import INFO
from torchvision.models import resnet18
import torch.utils.data as data
from tqdm import tqdm
import matplotlib.pyplot as plt
from utils import data_transform_input
from utils import data_transform_train as data_transform_test
import os

if __name__ == '__main__':
    data_flag = 'dermamnist'
    download = True

    info = INFO[data_flag]
    DataClass = getattr(medmnist, info['python_class'])
    task = info['task']
    n_classes = len(info['label'])
    
    print(f"Dataset: {data_flag}")
    print(f"Number Classes: {n_classes}")
    print("Class Labels:", info['label'])

    train_data = DataClass(split='train', transform=data_transform_input, download=download, size=224, mmap_mode='r')
    test_data = DataClass(split='test', transform=data_transform_test, download=download, size=224, mmap_mode='r')

    train_loader = data.DataLoader(dataset=train_data, batch_size=32, shuffle=True)
    test_loader = data.DataLoader(dataset=test_data, batch_size=32, shuffle=False)

    # Using a ResNet model because images come pre-processed to 224
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device == "cpu":
        print(f'WARNING: NOT TRAINING USING GPU')
        print(f'THIS IS MOST LIKELY BECAUSE YOU NEED TO INSTALL CUDA SUPPORT')
    model = resnet18(pretrained=True).to(device)

    model.fc = nn.Linear(model.fc.in_features, n_classes).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)

    train_losses = []
    test_accuracies = []
    learning_rates = []

    num_epochs = 50

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for inputs, targets in tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}"):
            inputs = inputs.to(device)
            targets = targets.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            targets = targets.squeeze().long()
            loss = criterion(outputs, targets)
            
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
        
        epoch_loss = running_loss / len(train_data)
        current_lr = optimizer.param_groups[0]['lr']
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}, LR: {current_lr:.6f}")
        
        train_losses.append(epoch_loss)
        learning_rates.append(current_lr)
        
        scheduler.step()

        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, targets in test_loader:
                inputs = inputs.to(device)
                targets = targets.to(device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs, 1)
                correct += (predicted == targets.squeeze().long()).sum().item()
                total += targets.size(0)
        test_accuracy = 100 * correct / total
        print(f"Epoch [{epoch+1}/{num_epochs}] Test Accuracy: {test_accuracy:.2f}%")
        test_accuracies.append(test_accuracy)
        
        model.train()

        checkpoint_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"Models", f"resnet18_{data_flag}_epoch{epoch+1}.pt")
        torch.save(model.state_dict(), checkpoint_path)
        print(f"Saved model checkpoint to {checkpoint_path}")

    print("Training complete!")

    epochs = range(1, num_epochs + 1)

    plt.figure(figsize=(12, 4))

    plt.figure()
    plt.plot(epochs, train_losses, marker='o', color='blue')
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.savefig('training_loss.png')
    plt.close()

    plt.figure()
    plt.plot(epochs, test_accuracies, marker='o', color='green')
    plt.title('Test Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.savefig('test_accuracy.png')
    plt.close()

    plt.figure()
    plt.plot(epochs, learning_rates, marker='o', color='red')
    plt.title('Learning Rate')
    plt.xlabel('Epoch')
    plt.ylabel('LR')
    plt.savefig('learning_rate.png')
    plt.close()