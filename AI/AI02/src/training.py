import os

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import AdamW
from tqdm import tqdm

from src.utils import TrainingConfig

LEARNING_RATE = 1e-3


def train(
    trainloader: DataLoader,
    validloader: DataLoader,
    model: nn.Module,
    train_cfg: TrainingConfig,
):
    criterion = nn.CrossEntropyLoss()
    optim = AdamW(model.parameters(), lr=LEARNING_RATE)

    best_acc = 0.0
    acc = 0.0

    for epoch in tqdm(range(train_cfg.num_epochs), desc="Epoch"):
        model.train()

        with tqdm(trainloader, desc="Train") as pbar:
            total_loss = 0.0
            acc = 0.0

            for landmarks, label in pbar:
                optim.zero_grad()

                output, _ = model(landmarks)
                print(output)
                loss = criterion(output, label)
                loss.backward()
                optim.step()

                total_loss += loss.item() / len(trainloader)
                # pylint: disable-next=no-member
                acc += (torch.argmax(output, dim=1) == label).sum().item() / len(
                    trainloader.dataset
                )

                pbar.set_postfix(loss=total_loss, acc=f"{acc * 100:.2f}%s")

        model.eval()

        with tqdm(validloader, desc="Valid") as pbar:
            total_loss = 0.0
            acc = 0.0

            with torch.no_grad():
                for landmarks, label in pbar:
                    output = model(landmarks)
                    loss = criterion(output, label)

                    total_loss += loss.item() / len(validloader)
                    # pylint: disable-next=no-member
                    acc += (torch.argmax(output, dim=1) == label).sum().item() / len(
                        validloader.dataset
                    )

                    pbar.set_postfix(loss=total_loss, acc=f"{acc * 100:.2f}%")

        if acc > best_acc:
            torch.save(model.state_dict(), os.path.join(train_cfg.save_dir, "best.pt"))
            tqdm.write("Saved best.")
            best_acc = acc

        if train_cfg.save_all:
            torch.save(
                model.state_dict(),
                os.path.join(train_cfg.save_dir, f"checkpoints/mnist_{epoch+1:03d}.pt"),
            )
