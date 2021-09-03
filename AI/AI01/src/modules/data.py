from dataclasses import dataclass

import numpy as np
import PIL.Image
import torch
from torch.utils.data import DataLoader, Dataset


def PIL_to_tensor(image: PIL.Image):
    im_torch = torch.tensor(np.array(image, dtype=np.float32))
    return im_torch

def CIFAR_transform(image: PIL.Image):
    x = PIL_to_tensor(image)
    x = torch.permute(x, (2, 0, 1))

    return x

@dataclass
class TrainingData():
    trainset: Dataset
    validset: Dataset
    trainloader: DataLoader
    validloader: DataLoader
