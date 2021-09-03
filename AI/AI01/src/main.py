import os

from torch.utils.data.dataloader import DataLoader
from torchvision.datasets.cifar import CIFAR10
from torchvision.datasets.mnist import MNIST
from efficientnet_pytorch import EfficientNet

import modules.models
import modules.train
from modules.data import PIL_to_tensor, CIFAR_transform, TrainingData

N_CLASSES = 10
DATASET_DIR = "/home/dimitri/Documents/A5-Courses/AI/AI01/dataset"
SAVE_PATH = "/home/dimitri/Documents/A5-Courses/AI/AI01/output"
NUM_EPOCHS = 100
SAVE_ALL = False
# DEVICE = "cuda:0"
DEVICE="cpu"


def main():
    os.makedirs(SAVE_PATH)

    model = modules.models.MLP(N_CLASSES)
    # model = modules.models.LeNet5(N_CLASSES)
    # model = modules.models.VGG16(N_CLASSES)
    # model = modules.models.ResNet15(N_CLASSES)
    # model = model = EfficientNet.from_pretrained('efficientnet-b1', num_classes=N_CLASSES)

    trainset_MNIST = MNIST(
        root=DATASET_DIR,
        train=True,
        transform=PIL_to_tensor,
        target_transform=None,
        download=True
    )
    validset_MNIST = MNIST(
        root=DATASET_DIR,
        train=False,
        transform=PIL_to_tensor,
        target_transform=None,
        download=True
    )
    training_data_MNIST = TrainingData(trainset=trainset_MNIST,
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
                                       ))

    trainset_CIFAR = CIFAR10(
        root=DATASET_DIR,
        train=True,
        transform=CIFAR_transform,
        target_transform=None,
        download=True
    )
    validset_CIFAR = CIFAR10(
        root=DATASET_DIR,
        train=False,
        transform=CIFAR_transform,
        target_transform=None,
        download=True
    )
    training_data_CIFAR = TrainingData(trainset=trainset_CIFAR,
                                       validset=validset_CIFAR,
                                       trainloader=DataLoader(
                                           trainset_CIFAR,
                                           batch_size=32,
                                           shuffle=True,
                                           num_workers=2,
                                           pin_memory=True,
                                       ),
                                       validloader=DataLoader(
                                           validset_CIFAR,
                                           batch_size=32,
                                           shuffle=True,
                                           num_workers=2,
                                           pin_memory=True,
                                       ))

    modules.train.train(model=model,
                        training_data=training_data_MNIST,
                        # training_data=training_data_CIFAR,
                        save_path=SAVE_PATH,
                        num_epochs=NUM_EPOCHS,
                        save_all=SAVE_ALL,
                        device=DEVICE)


if __name__ == "__main__":
    main()
