import numpy as np
import PIL.Image
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision.datasets import MNIST


def PIL_to_tensor(image: PIL.Image):
    im_torch = torch.tensor(np.array(image, dtype=np.float32))
    return im_torch


class TrainingData():
    trainset: Dataset
    validset: Dataset
    trainloader: DataLoader
    validloader: DataLoader

    def __init__(self, dataset_dir):
        self.trainset = MNIST(
            root=dataset_dir,
            train=True,
            transform=PIL_to_tensor,
            target_transform=None,
            download=True
        )

        self.validset = MNIST(
            root=dataset_dir,
            train=False,
            transform=PIL_to_tensor,
            target_transform=None,
            download=True
        )

        self.trainloader = DataLoader(
            self.trainset,
            batch_size=32,
            shuffle=True,
            num_workers=6,
            pin_memory=True,
        )

        self.validloader = DataLoader(
            self.validset,
            batch_size=32,
            shuffle=True,
            num_workers=6,
            pin_memory=True,
        )
