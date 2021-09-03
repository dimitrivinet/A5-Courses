import os

import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.utils.data import DataLoader
from tqdm import tqdm

import modules.data as data

LEARNING_RATE = 1e-3


def train(model: nn.Module, dataset_dir: os.PathLike, save_path: os.PathLike, num_epochs: int, save_all: bool = False):
    training_data = data.TrainingData(dataset_dir)

    criterion = nn.CrossEntropyLoss()
    optim = AdamW(model.parameters(), lr=LEARNING_RATE)

    best_acc = 0.0
    acc = 0.0

    for epoch in tqdm(range(num_epochs), desc='Epoch'):
        model.train()

        with tqdm(training_data.trainloader, desc='Train') as pbar:
            total_loss = 0.0
            acc = 0.0

            for landmarks, label in pbar:
                optim.zero_grad()

                output = model(landmarks)
                loss = criterion(output, label)
                loss.backward()
                optim.step()

                total_loss += loss.item() / len(training_data.trainloader)
                acc += (
                    torch.argmax(output, dim=1) == label
                ).sum().item() / len(training_data.trainset)

                pbar.set_postfix(loss=total_loss, acc=f"{acc * 100:.2f}%s")

        model.eval()

        with tqdm(training_data.validloader, desc='Valid') as pbar:
            total_loss = 0.0
            acc = 0.0

            with torch.no_grad():
                for landmarks, label in pbar:
                    output = model(landmarks)
                    loss = criterion(output, label)

                    total_loss += loss.item() / len(training_data.validloader)
                    acc += (
                        torch.argmax(output, dim=1) == label
                    ).sum().item() / len(training_data.validset)

                    pbar.set_postfix(loss=total_loss, acc=f"{acc * 100:.2f}%")

        if acc > best_acc:
            torch.save(model.state_dict(), os.path.join(save_path, "best.pt"))
            tqdm.write('Saved best.')
            best_acc = acc

        if save_all:
            torch.save(
                model.state_dict(),
                os.path.join(save_path, f"checkpoints/mnist_{epoch+1:03d}.pt"))
