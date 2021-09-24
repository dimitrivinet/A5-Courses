import os

from dataclasses import dataclass

@dataclass
class TrainingConfig:
    """Config options for training."""

    num_epochs: int
    save_dir: os.PathLike
    save_all: bool = False
