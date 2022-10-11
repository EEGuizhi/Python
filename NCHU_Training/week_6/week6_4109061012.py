#4109061012 陳柏翔

import torch
import numpy
from torch import nn
from torch.utils.data import DataLoader
from torchvision import transforms
import matplotlib.pyplot as plt
import torchvision


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        # Layer 1 (Convolution):
        # Input Channel=1, Output Channel=6, Kernal=5*5, Stride=1, Padding=2
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 6, 5, 1, 2),
            nn.ReLU()
        )
        # Layer 2 (Max Pool): Kernal=2*2, Stride=2
        self.layer2 = nn.MaxPool2d(2, 2)
        # Layer 3 (Convolution): Input Channel=6, Output Channel=16, Kernal=5*5, Stride=1, Padding=0
        self.layer3 = nn.Sequential(
            nn.Conv2d(6, 16, 5, 1, 0),
            nn.ReLU()
        )
        # Layer 4 (Max Pool): Kernal=2*2, Stride=2
        self.layer4 = nn.MaxPool2d(2, 2)
        # Layer 5 (Fully connected & ReLU): input 16*5*5, output 120
        self.layer5 = nn.Sequential(
            nn.Linear(16*5*5, 120),
            nn.ReLU()
        )
        # Layer 6 (Fully connected): input 120, output 84
        self.layer6 = nn.Sequential(
            nn.Linear(120, 84),
            nn.ReLU()
        )
        # Layer 7 Output (加Softmax Loss會比較高 所以拿掉)
        self.out = nn.Linear(84, 10)

    def forward(self, x):
        x = self.layer1(x)  # (1, 28, 28) => (6, 28, 28)
        x = self.layer2(x)  # (6, 28, 28) => (6, 14, 14)
        x = self.layer3(x)  # (6, 14, 14) => (16, 10, 10)
        x = self.layer4(x)  # (16, 10, 10) => (16, 5, 5)
        x = x.view(-1, 16*5*5)  # Flatten
        x = self.layer5(x)  # (16, 5, 5) => (120)
        m = nn.Dropout(p=0.1)  # Dropout Layer
        x = m(x)
        x = self.layer6(x)  # (120) => (84)
        x = x.view(-1, 84)
        output = self.out(x)  # (84) => (10)
        return output


if __name__ == "__main__":
    
    DOWNLOAD = False
    BATCH = 64
    LR = 1e-3
    EPOCH = 3
    
    # Download
    training_data = torchvision.datasets.MNIST(
        root = './mnist', train = True, transform = transforms.ToTensor(), download = DOWNLOAD
    )
    test_data = torchvision.datasets.MNIST(
        root = './mnist', train = False, transform = transforms.ToTensor(), download = DOWNLOAD
    )
    train_dataloader = DataLoader(training_data, batch_size=BATCH, shuffle=True)
    test_dataloader = DataLoader(test_data, batch_size=BATCH, shuffle=True)
    
    # Device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f">> Using {device} device")
    model = CNN().to(device)

    # Training
    model.train()
    optimization = torch.optim.Adam(model.parameters(), lr = LR)
    loss_func = nn.CrossEntropyLoss()
    
    
    print(">> Training...")
    Loss = []
    Mean_Loss = []
    i = 0
    for x_train, outputs in train_dataloader:
        x_train = x_train.to(device)
        outputs = outputs.to(device)
        y_train = model(x_train)
        loss = loss_func(y_train, outputs)
        optimization.zero_grad()
        loss.backward()
        optimization.step()

        i += 1
        if (i-1) % 100 == 0:
            print(f"Batch：{(i-1)*64}/60000 ", "| Loss：%.4f" % loss.item())
        Loss.append(loss.item())
        if len(Loss) < 50:
            Mean_Loss.append(sum(Loss)/len(Loss))
        else:
            Mean_Loss.append(sum(Loss[-50:-1])/50)
            
    plt.title("Mean Loss | Window Size = 50")
    plt.plot(numpy.array(Mean_Loss))


    print(">> Testing...")
    with torch.no_grad():
        correct = 0
        total = 0
        for x_test, y_test in test_dataloader:
            x_test = x_test.to(device)
            y_test = y_test.to(device)
            outputs = model(x_test)
            nums, pred = torch.max(outputs.data, dim=1)
            for i in range(pred.size(0)):
                total += 1
                correct += 1 if pred[i] == y_test[i] else 0
                
        print('Acc：{} %'.format(correct / total * 100))

    plt.show()
