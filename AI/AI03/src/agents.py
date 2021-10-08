from __future__ import annotations

import pickle
from abc import ABC, abstractmethod

import gym
import numpy as np
import tqdm


class Agent(ABC):
    """Base class for a Q learning agent."""

    env: gym.Env  # gym env
    lr: float  # learing rate
    df: float  # discount factor
    eps: float  # epsilon greedy
    Q: np.ndarray  # Q matrix

    def __init__(self, env: str, lr: float, df: float):
        self.env = gym.make(env)
        self.lr = lr
        self.df = df

        self.eps = 0.95

        self.n_actions = self.env.action_space.n
        self.n_states = self.env.observation_space.n

        self.Q = np.zeros((self.n_states, self.n_actions))

    def update_Q(self, action, current_state: int, next_state: int, reward: int):
        """Update Q matrix."""

        self.Q[current_state, action] += self.lr * (
            reward
            + self.df * (self.Q[next_state].max())
            - self.Q[current_state, action]
        )

    def update_eps(self):
        """Update greedy epsilon."""

        self.eps *= self.eps

    def fit(self, n_episodes: int):
        """Train on n_episodes episodes."""

        num_iter: int
        all_num_iters = []

        with tqdm.tqdm(range(n_episodes), desc="Episodes") as pbar:
            for _ in pbar:
                s, done = self.env.reset(), False

                num_iter = 0

                while not done:
                    num_iter += 1

                    a = self(s)
                    s_next, r, done, *_ = self.env.step(a)
                    self.update_Q(a, s, s_next, r)

                    s = s_next

                self.update_eps()

                all_num_iters.append(num_iter)
                pbar.set_postfix(
                    num_iter=num_iter,
                    min_num_iter=min(all_num_iters),
                    max_num_iter=max(all_num_iters),
                )

                self.env.close()

    def save(self, output_path: str):
        """Save trained Agent in pickle format."""

        with open(output_path, 'wb') as outp:
            pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, agent_path: str) -> Agent:
        """Load trained Agent from pickle file."""

        with open(agent_path, 'rb') as inp:
            agent: Agent = pickle.load(inp)

        return agent


    @abstractmethod
    def __call__(self, state: int) -> int:
        """Get action for state."""

    def test(self):
        """Test trained model."""

        s, done = self.env.reset(), False
        self.env.render()
        input()
        while not done:
            a = self(s)
            s, _, done, *_ = self.env.step(a)
            self.env.render()

            input()

        self.env.close()


class RandomAgent(Agent):
    """Random agent."""

    def __call__(self, state: int) -> int:
        n = np.random.uniform(0, 1)
        if n < self.eps:
            return self.env.action_space.sample()
        return int(np.argmax(self.Q[state]))
