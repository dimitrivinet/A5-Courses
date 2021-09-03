import torch
import torch.nn as nn


class MLP(nn.Module):
    def __init__(self, n_classes):
        super(MLP, self).__init__()
        self.n_classes = n_classes

        self.MLP = nn.Sequential(
            nn.Linear(28*28, 16*16),
            nn.ReLU(),
            nn.Linear(16*16, 8*8),
            nn.ReLU(),

            nn.Dropout(0.2),

            nn.Linear(8*8, 4*4),
            nn.ReLU(),

            nn.Linear(4*4, n_classes)
        )

    def forward(self, x: torch.Tensor):
        x = x.view(x.shape[0], -1)

        x = self.MLP(x)

        return x


class LeNet5(nn.Module):
    def __init__(self, n_classes):
        super(LeNet5, self).__init__()
        self.n_classes = n_classes

        self.conv = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=6,
                      kernel_size=(5, 5), padding=2),
            nn.ReLU(),

            nn.AvgPool2d(kernel_size=2, stride=2),

            nn.Conv2d(in_channels=6, out_channels=16, kernel_size=(5, 5)),
            nn.ReLU(),

            nn.AvgPool2d(kernel_size=2, stride=2),

            nn.Conv2d(in_channels=16, out_channels=120,
                      kernel_size=(5, 5), padding=0),
            nn.ReLU()
        )

        self.fc = nn.Sequential(
            nn.Linear(in_features=120, out_features=84),
            nn.ReLU(),

            nn.Linear(in_features=84, out_features=self.n_classes),
            nn.ReLU()
        )

    def forward(self, x: torch.Tensor):
        x = x.view(x.shape[0], 1, x.shape[1], x.shape[2])
        x = self.conv(x)
        x = x.view(x.shape[0], -1)
        x = self.fc(x)

        return x


class VGG16(nn.Module):
    def __init__(self, n_classes):
        super(VGG16, self).__init__()
        self.n_classes = n_classes

        self.conv = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=64,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(in_channels=64, out_channels=128,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=128, out_channels=128,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(in_channels=128, out_channels=256,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=256, out_channels=256,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=256, out_channels=256,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(in_channels=256, out_channels=512,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(in_channels=512, out_channels=512,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )

        self.fc = nn.Sequential(
            nn.Linear(512, 4096),
            nn.ReLU(),
            nn.Linear(4096, 4096),
            nn.ReLU(),
            nn.Linear(4096, 4096),
            nn.ReLU(),

            nn.Linear(4096, 1000),
            nn.ReLU(),

            nn.Linear(1000, self.n_classes),
            nn.ReLU()
        )

    def forward(self, x):
        x = torch.permute(x, (0, 3, 1, 2))
        x = self.conv(x)
        x = x.view(x.shape[0], -1)
        x = self.fc(x)

        return x


class ResNet15(nn.Module):
    def __init__(self, n_classes):
        super(ResNet15, self).__init__()
        self.n_classes = n_classes

        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=64,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64,
                      kernel_size=3, padding=1),
            nn.ReLU(),
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=128, out_channels=128,
                      kernel_size=3, padding=1),
            nn.ReLU(),
        )

        self.conv3 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=256,
                      kernel_size=3, padding=1),
            nn.ReLU()
        )

        self.conv3_5 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=256,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=256, out_channels=256,
                      kernel_size=3, padding=1),
            nn.ReLU(),
        )

        self.conv4 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=512,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512,
                      kernel_size=3, padding=1),
            nn.ReLU(),
        )

        self.conv5 = nn.Sequential(
            nn.Conv2d(in_channels=512, out_channels=512,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512,
                      kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=512, out_channels=512,
                      kernel_size=3, padding=1),
            nn.ReLU(),
        )

        self.fc = nn.Sequential(
            nn.Linear(512, 4096),
            nn.ReLU(),
            nn.Linear(4096, 4096),
            nn.ReLU(),
            nn.Linear(4096, 4096),
            nn.ReLU(),

            nn.Linear(4096, 1000),
            nn.ReLU(),

            nn.Linear(1000, self.n_classes),
            nn.ReLU()
        )

    def forward(self, x):
        x = torch.permute(x, (0, 3, 1, 2))

        x = self.conv1(x)
        x = nn.MaxPool2d(2, 2)(x)

        old = x.clone()
        x = self.conv2(x)
        x = old + x
        x = nn.ReLU()(x)
        x = nn.MaxPool2d(2, 2)(x)

        old = x.clone()
        x = self.conv3(x)
        x = old + x
        x = nn.ReLU()(x)
        x = nn.MaxPool2d(2, 2)(x)

        old = x.clone()
        x = self.conv4(x)
        x = old + x
        x = nn.ReLU()(x)
        x = nn.MaxPool2d(2, 2)(x)

        old = x.clone()
        x = self.conv5(x)
        x = old + x
        x = nn.ReLU()(x)
        x = nn.MaxPool2d(2, 2)(x)

        x = x.view(x.shape[0], -1)
        x = self.fc(x)

        return x
