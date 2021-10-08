import numpy as np
from typing import List, NamedTuple

import torch


class Transition(NamedTuple):
    """Representation of a transition between states."""

    s: torch.Tensor
    a: torch.Tensor
    s_next: torch.Tensor
    r: torch.Tensor


class ReplayMemory:
    """Replay memory for Deep Q Learning."""

    maxsize: int
    memory: List[Transition]

    def __init__(self, maxsize: int = 256):
        self.maxsize = maxsize

        self.memory = []
        self.idx = 0

    def __len__(self) -> int:
        return len(self.memory)

    def push(self, transition: Transition) -> None:
        """Add transition to memory."""

        if len(self.memory) < self.maxsize:
            self.memory.append(None)  # type: ignore

        self.memory[self.idx] = transition
        self.idx = (self.idx + 1) % self.maxsize

    def sample(self, batch_size: int) -> List[Transition]:
        """Sample random transitions from memory."""

        idxs = np.random.choice(len(self.memory), size=batch_size)
        return [self.memory[idx] for idx in idxs]
