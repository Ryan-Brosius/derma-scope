import torch
import torchvision.transforms as transforms
import medmnist
from medmnist import INFO
from torchvision.models import resnet18
import torch.utils.data as data
from tqdm import tqdm
from utils import data_transform_input as data_transform

if __name__ == "__main__":
    data_flag = 'dermamnist'
    info = INFO[data_flag]
    DataClass = getattr(medmnist, info['python_class'])
    task = info['task']
    n_classes = len(info['label'])

    print(f"Dataset: {data_flag}")
    print(f"Number of Classes: {n_classes}")
    print("Class Labels:", info['label'])

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    test_data = DataClass(split='test', transform=data_transform, download=True, size=224, mmap_mode='r')
    test_loader = data.DataLoader(dataset=test_data, batch_size=32, shuffle=False)
    model = resnet18(num_classes=n_classes).to(device)
    checkpoint_path = r'Models\resnet18_dermamnist_epoch49_Best_New.pt'
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()
    
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in tqdm(test_loader, desc="Evaluating"):
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            labels = labels.squeeze()
            correct += (predicted == labels).sum().item()
            total += labels.size(0)
        
    accuracy = correct / total
    print(f'\nTest Accuracy: {accuracy*100:.2f}% on {total} samples')
