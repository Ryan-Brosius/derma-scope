![DermaScope Logo](frontend/images/logo.png)

## Overview
Millions around the world lack access to dermatologists, leading to late diagnoses of serious skin conditions. Our AI-powered skin lesion detection app bridges this gap by providing instant, affordable, and accessible skin analysis. Simply upload a picture, and our technology predicts potential concerns—empowering early detection, especially in underserved communities. With this tool, we’re bringing life-saving dermatological insights to those who need them most.

Our model is trained on the HAM10000 dataset, which comprises data on seven different types of skin lesions, curated by medical professionals. We fine-tuned a PyTorch implementation of ResNet18 over 50 epochs, incorporating noise filtering during each training pass to overcome the challenges posed by the small dataset. These efforts have enabled us to achieve an accuracy rate of approximately 90% on our test evaluation.

## Setup Instructions

### 1. Create a Virtual Environment
It is recommended to use a virtual environment.

```sh
python -m venv venv
```

Activate the environment:
- **Windows**:
  ```sh
  venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```sh
  source venv/bin/activate
  ```

### 2. Install Dependencies

After activating the virtual environment, install the required dependencies using:

```sh
pip install -r requirements.txt
```

### 3. Run the Application
To start the application, use the following command:

```sh
python main.py
```

## Model Images
Below are visual representations of our model pipeline and training progress:

### Report Pipeline
![Report Pipeline](frontend/images/Report_Pipeline.webp)

### ResNet18 Model Architecture
![ResNet18 Model](frontend/images/ResNet18_Model.webp)

### Test Accuracy
![Test Accuracy](frontend/images/test_accuracy.png)

### Training Loss
![Training Loss](frontend/images/training_loss.png)