import torch
import torch.nn as nn


class MLP(nn.Module):
    def __init__(self, n_classes):
        super(MLP, self).__init__()
        self.n_classes = n_classes

        self.MLP = nn.Sequential(
            nn.Linear(28*28, 1024),
            nn.ReLU(),

            nn.Linear(1024, 2048),
            nn.ReLU(),

            nn.Linear(2048, 4096),
            nn.ReLU(),

            nn.Linear(4096, 2048),
            nn.ReLU(),

            nn.Linear(2048, 1024),
            nn.ReLU(),

            nn.Dropout(0.2),

            nn.Linear(1024, 512),
            nn.ReLU(),

            nn.Linear(512, 256),
            nn.ReLU(),

            nn.Linear(256, 128),
            nn.ReLU(),

            nn.Linear(128, 64),
            nn.ReLU(),

            nn.Dropout(0.2),

            nn.Linear(64, n_classes),
            nn.ReLU()
        )

    def forward(self, x: torch.Tensor):
        x = x.view(x.shape[0], -1)

        x = self.MLP(x)

        return x
