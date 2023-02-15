import numpy as np
import torch
import torchvision
import matplotlib.pyplot as plt

from torch.utils.data import DataLoader


class LeNet5(torch.nn.Module):
    def __init__(self):
        super(LeNet5, self).__init__()
        #
        # Define network structure
        #
        self.layer1 = torch.nn.Conv2d(1, 6, 5)
        self.layer2 = torch.nn.Conv2d(6, 16, 5)
        self.layer3 = torch.nn.Linear(256, 120)
        self.layer4 = torch.nn.Linear(120, 84)
        self.layer5 = torch.nn.Linear(84, 10)

        self.flatten = torch.nn.Flatten()
        self.pooling = torch.nn.MaxPool2d(2, 2)

    def forward(self, in_feature):
        out_feature = self.pooling(self.layer1(in_feature))
        out_feature = self.pooling(self.layer2(out_feature))
        out_feature = self.layer3(self.flatten(out_feature))
        out_feature = self.layer4(out_feature)
        out_feature = self.layer5(out_feature)

        return out_feature


# Define training parameters
batch_size = 64
epoch = 100
lr = 1e-3

loss_point = []
loss_window = []

# Create model
model = LeNet5()

# Loading dataset and setting data loader
train_dataset = torchvision.datasets.MNIST('./mnist',
                                           train=True,
                                           transform=torchvision.transforms.ToTensor(),
                                           download=True)

test_dataset = torchvision.datasets.MNIST('./mnist',
                                          train=False,
                                          transform=torchvision.transforms.ToTensor(),
                                          download=True)

train_dataloader = DataLoader(train_dataset,
                              batch_size=batch_size,
                              shuffle=True)

test_dataloader = DataLoader(test_dataset,
                             batch_size=batch_size,
                             shuffle=True)

# Define loss function and optimization
loss_fn = torch.nn.CrossEntropyLoss()
optim = torch.optim.Adam(model.parameters(), lr=lr)

#
# Create training loop
#
print("training...")
for batch, (image, label) in enumerate(train_dataloader):
    # Compute prediction and loss
    predict = model.forward(image)
    loss = loss_fn(predict, label)

    # Optimize the model
    loss.backward()
    optim.step()
    optim.zero_grad()

    if batch > 50:
        loss_window.pop(0)
        loss_window.append(loss.item())
        loss_point.append(sum(loss_window)/len(loss_window))
    else:
        loss_window.append(loss.item())
        loss_point.append(sum(loss_window) / len(loss_window))

    if batch % 100 == 0:
        print("Batch : {}/{} | Loss : {:0.4f}".format(batch * batch_size, len(train_dataset), loss.item()))

#
# Create testing loop
#
print("(testing...)")
with torch.no_grad():
    predictCorrect = 0
    for image, label in test_dataloader:
        # Compute prediction and loss
        predict = model.forward(image)
        predict = predict.argmax(axis=1)

        # Calculate matches
        match = (predict == label)
        predictCorrect += match.sum()

    print("Acc : {:2.2f}%".format(100 * predictCorrect / len(test_dataset)))

plt.title("Mean Loss | Window Size = 50")
plt.plot(loss_point)
plt.show()
