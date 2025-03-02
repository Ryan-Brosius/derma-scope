import torch
from torchvision.models import resnet18
from PIL import Image
from dermascope_model.utils import data_transform_input as data_transform
import os

class_labels = {0: 'actinic keratoses and intraepithelial carcinoma',
                1: 'basal cell carcinoma',
                2: 'benign keratosis-like lesions',
                3: 'dermatofibroma',
                4: 'melanoma',
                5: 'melanocytic nevi',
                6: 'vascular lesions'}

n_classes = 7 

def classify_image(image: Image.Image):
    image = data_transform(image)
    image = image.unsqueeze(0)

    model = resnet18(num_classes=n_classes).to('cpu')
    checkpoint_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"Models", f"resnet18_dermamnist_epoch49_Best_New.pt")
    model.load_state_dict(torch.load(checkpoint_path, map_location=torch.device('cpu')))
    model.eval()

    with torch.no_grad():
        output = model(image)
        prediction = torch.argmax(output, dim=1).item()

    return class_labels[prediction]

def classify_image_with_confidence(image: Image.Image):
    image = data_transform(image)
    image = image.unsqueeze(0)

    model = resnet18(num_classes=n_classes).to('cpu')
    checkpoint_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Models", "resnet18_dermamnist_epoch49_Best_New.pt")
    model.load_state_dict(torch.load(checkpoint_path, map_location=torch.device('cpu')))
    model.eval()

    with torch.no_grad():
        output = model(image)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        prediction = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0, prediction].item()

    return {"Prediction": class_labels[prediction], "Confidence": confidence}


if __name__ == "__main__":
    ## Sanity Check for myself lol

    import os
    FILEPATH = r'TestImages'
    files = os.listdir(FILEPATH)
    files = [os.path.join(FILEPATH, f) for f in files if os.path.isfile(os.path.join(FILEPATH, f))]
    padding = len(max(files, key=len)) + 3

    for f in files:
        result = classify_image(f)
        print(f'{f:<{padding}} {result}')

