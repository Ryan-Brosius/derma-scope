import torchvision.transforms as transforms

# Trying to augment the data with small variations each time
# so we dont just learn out dataset and instead **learn** what
# we are trying to predict
data_transform_train = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

# Transforms our data in a regular context to make it easy to
# work with regular image data in the future
# needs to be 224 x 224 for resnet-18 or it will cry :(
data_transform_input = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])