# 4109061012 陳柏翔
import os
import pandas as pd
import torch
import torch.nn as nn
from torchvision.io import read_image
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision import models


EPOCH = 7
PATH = "week_7/birds_dataset"
FILE_PATH = "week_7/birds_dataset/birds.csv"
BATCH_SIZE = 128
LR = 1e-3


class Bird_Dataset(Dataset):
    def __init__(self, annotations_file, img_dir, transform=None, mode="train"):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_labels = self.img_labels[self.img_labels["data set"] == mode]
        self.img_dir = img_dir
        self.transform = transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 1])
        image = read_image(img_path)
        label = self.img_labels.iloc[idx, 0]
        if self.transform:
            image = self.transform(image)
        return image, label


class ResNet18(nn.Module):
    def __init__(self, num_classes=400):
        super(ResNet18, self).__init__()
        self.net = models.resnet18(num_classes=num_classes)

    def forward(self, x):
        x = self.net(x)
        return x


if __name__ == "__main__":
    
    # Device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f">> Using {device} device")
    
    # Loading Dataset
    train_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((112, 112)),
        transforms.RandomHorizontalFlip(p=0.1),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    test_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((112, 112)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    train_set = Bird_Dataset(FILE_PATH, PATH, transform=train_transform, mode="train")
    train = DataLoader(train_set, batch_size = BATCH_SIZE, shuffle = True)
    valid_set = Bird_Dataset(FILE_PATH, PATH, transform=train_transform, mode="valid")
    valid = DataLoader(valid_set, batch_size = BATCH_SIZE, shuffle = True)
    test_set = Bird_Dataset(FILE_PATH, PATH, transform=test_transform, mode="test")
    test = DataLoader(test_set, batch_size = BATCH_SIZE, shuffle = True)
    
    # Create model
    model = ResNet18().to(device)
    
    # Define loss function and optimization
    loss_func = nn.CrossEntropyLoss()
    optimization = torch.optim.Adam(model.parameters(), lr = LR)
    
    # Train
    print(">> Training...")
    for k in range(EPOCH):
        for i, (inputs, label) in enumerate(train):
            model.train()
            inputs = inputs.to(device)
            label = label.to(device)
            
            # Compute prediction and loss
            outputs = model(inputs)
            loss = loss_func(outputs, label)

            # Optimize the model
            optimization.zero_grad()
            loss.backward()
            optimization.step()

            if i % 10 == 0:
                print(f"Epoch：{k+1} | Batch：{i*BATCH_SIZE}/{len(train_set)} | Loss：{round(loss.item(), 3)}")

        print(">> Validation...")
        with torch.no_grad():
            correct = 0
            total = 0
            for i, (inputs, label) in enumerate(valid):
                model.eval()
                inputs = inputs.to(device)
                label = label.to(device)
                ouputs = model(inputs)
                nums, pred = torch.max(ouputs.data, dim=1)
                for i in range(pred.size(0)):
                    total += 1
                    correct += 1 if pred[i] == label[i] else 0
                    
            print(f"Epoch：{k+1} | Acc：{correct / total * 100} % \n")

    print(">> Testing...")
    with torch.no_grad():
        correct = 0
        total = 0
        for i, (inputs, label) in enumerate(valid):
            inputs = inputs.to(device)
            label = label.to(device)
            ouputs = model(inputs)
            nums, pred = torch.max(ouputs.data, dim=1)
            for i in range(pred.size(0)):
                total += 1
                correct += 1 if pred[i] == label[i] else 0
                
        print(f"Acc：{correct / total * 100} %")
