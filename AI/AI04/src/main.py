import os
from pathlib import Path

from torch.utils.data.dataloader import DataLoader
from torchvision.datasets.mnist import MNIST

import modules.models
import modules.train
from modules.data import PIL_to_tensor, TrainingData

FILE = Path(__file__).resolve()
N_CLASSES = 10
DATASET_DIR = FILE.parent / "dataset"
SAVE_PATH = FILE.parent / "output"
NUM_EPOCHS = 100
SAVE_ALL = False
# DEVICE = "cuda:0"
DEVICE = "cpu"


def main():
    os.makedirs(SAVE_PATH, exist_ok=True)

    model = modules.models.LeNet5(N_CLASSES)

    trainset_MNIST = MNIST(
        root=DATASET_DIR,
        train=True,
        transform=PIL_to_tensor,
        target_transform=None,
        download=True,
    )
    validset_MNIST = MNIST(
        root=DATASET_DIR,
        train=False,
        transform=PIL_to_tensor,
        target_transform=None,
        download=True,
    )
    training_data_MNIST = TrainingData(
        trainset=trainset_MNIST,
        validset=validset_MNIST,
        trainloader=DataLoader(
            trainset_MNIST,
            batch_size=32,
            shuffle=True,
            num_workers=2,
            pin_memory=True,
        ),
        validloader=DataLoader(
            validset_MNIST,
            batch_size=32,
            shuffle=True,
            num_workers=2,
            pin_memory=True,
        ),
    )

    modules.train.train(
        model=model,
        training_data=training_data_MNIST,
        # training_data=training_data_CIFAR,
        save_path=SAVE_PATH,
        num_epochs=NUM_EPOCHS,
        save_all=SAVE_ALL,
        device=DEVICE,
    )


if __name__ == "__main__":
    main()
