"""
from https://github.com/Nathaniel-Slyte/IRM_Courses/blob/master/Deep_Learning/deepqlearning.py
"""

from itertools import count

import gym
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
import torchvision.transforms as T
from torch import nn
from torch.optim import AdamW
from tqdm import tqdm

from utils import ReplayMemory, Transition

# pylint: disable = not-callable


class QNet(nn.Module):
    """Q network model."""

    def __init__(self, actions: int) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=7, stride=4, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),
            nn.Conv2d(16, 32, kernel_size=5, stride=2),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=5, stride=2),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
        )
        self.fc = nn.Sequential(
            nn.Linear(32 * 5 * 5, 512), nn.ReLU(inplace=True), nn.Linear(512, actions)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Compute model forward."""

        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)


def get_screen(env: gym.Env) -> torch.Tensor:
    """Get gym env render as RBG array."""

    render = env.render(mode="rgb_array").transpose((2, 0, 1))
    render = torch.from_numpy(render.astype(np.float32) / 255.0)
    render = render.unsqueeze(0)
    _, _, H, W = render.size()  # B, C, H, W
    render = T.functional.center_crop(render, (min(W, H), min(W, H)))
    render = T.functional.resize(render, (int(0.3 * min(W, H)), int(0.3 * min(W, H))))
    return render


DEVICE = "cpu"
EPISODES = 1_000
CAPACITY = 10_000
BATCH_SIZE = 32
alpha = 1e-3
gamma = 0.99
epsilon = 1.0
epsilon_decay = 0.90

GYM_ENV = gym.make("CartPole-v1")

q_network = QNet(actions=GYM_ENV.action_space.n).to(DEVICE)
replay_memory = ReplayMemory(maxsize=CAPACITY)
optim = AdamW(q_network.parameters(), lr=alpha)

# ====== Train Model
history = []

with tqdm(range(EPISODES), "Episode") as pbar:
    for epsode in pbar:
        GYM_ENV.reset()  # Reset Environment
        done = False  # Is Game Done?

        last_screen = get_screen(GYM_ENV)  # Screen t-1
        current_screen = get_screen(GYM_ENV)  # Screen t
        s = (current_screen - last_screen).to(DEVICE)  # Compute State t

        # ====== While Episode
        for t in count():
            # Explore or Exploit
            with torch.no_grad():
                a = (
                    torch.tensor([[np.random.randint(GYM_ENV.action_space.n)]])
                    .long()
                    .to(DEVICE)
                    if np.random.uniform(0, epsilon)
                    else torch.argmax(q_network(s), dim=1).view(1, 1)
                )

            # Collect Reward
            _, r, done, *_ = GYM_ENV.step(a.item())
            r = torch.tensor([r]).to(DEVICE)

            last_screen = current_screen  # Screen t-1 = Screen t
            current_screen = get_screen(GYM_ENV)  # Screen t   = Screen t+1
            s_next = (
                (current_screen - last_screen).to(DEVICE) if not done else None
            )  # Compute State t+1

            replay_memory.push(
                Transition(s, a, s_next, r)
            )  # Add Transition to Replay Memory
            s = s_next  # State t = State t+1

            # ====== Optimize Model
            if len(replay_memory) >= BATCH_SIZE:
                # Sample Transitions
                transitions = replay_memory.sample(BATCH_SIZE)

                # Fuse Transition for Batch
                batch = Transition(*zip(*transitions))
                batch_s = torch.cat(batch.s)  # Fuse State for Batch
                batch_a = torch.cat(batch.a)  # Fuse Action for Batch
                batch_r = torch.cat(batch.r)  # Fuse Reward for Batch

                nf = lambda s: s is not None
                nf_mask = (
                    torch.tensor(list(map(nf, batch.s_next))).bool().to(DEVICE)
                )  # Create Non-Final Mask
                nf_s_next = torch.cat(list(filter(nf, batch.s_next))).to(
                    DEVICE
                )  # Collect Non-Final Next State

                # Compute Actual Q Values Estimations
                q_values = q_network(batch_s).gather(1, batch_a)

                # Compute Expected Q Values Estimations
                q_values_next = torch.zeros(BATCH_SIZE).to(DEVICE)
                q_values_next[nf_mask] = q_network(nf_s_next).max(dim=1)[0]
                𝔼_q_values = (batch_r + gamma * q_values_next).unsqueeze(1)

                # Optimization Process
                optim.zero_grad()
                loss = F.mse_loss(q_values, 𝔼_q_values)
                loss.backward()
                for parameter in q_network.parameters():
                    parameter.grad.data.clamp_(-1, 1)
                optim.step()

            if done:
                history.append(t + 1)
                break

        # Update Greedy Epsilon
        epsilon *= epsilon_decay
        pbar.set_postfix(epsilon=epsilon)


plt.plot(history)
plt.show()

torch.jit.save(torch.jit.trace(q_network, batch_s), "output/dqn.pt")

# ====== Test Model
q_network.eval()

for i in range(10):
    print(f"\n====== TEST[{i+1:02d}/{10}]")
    GYM_ENV.reset()
    done = False

    last_screen = get_screen(GYM_ENV)
    current_screen = get_screen(GYM_ENV)
    s = (current_screen - last_screen).to(DEVICE)

    while not done:
        with torch.no_grad():
            a = torch.argmax(q_network(s), dim=1).item()
        _, _, done, *_ = GYM_ENV.step(a)

        last_screen = current_screen
        current_screen = get_screen(GYM_ENV)
        s = (current_screen - last_screen).to(DEVICE) if not done else None

        GYM_ENV.render()
GYM_ENV.close()
