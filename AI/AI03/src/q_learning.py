from __future__ import annotations

import os
import pickle

import gym
import numpy as np
import tqdm


TAXI = "Taxi-v3"
CARTPOLE = "CartPole-v0"

LR = 1.0
DF = 0.5
N_EPISODES = 10_000


class QLearningAgent:
    """Class for a Q learning agent."""

    env: gym.Env  # gym env
    n_actions: int
    n_states: int
    lr: float  # learing rate
    df: float  # discount factor
    eps: float  # greedy epsilon
    Q: np.ndarray  # Q matrix

    def __init__(
        self,
        env: str,
        n_actions: int,
        n_states: int,
        lr: float = 1.0,
        df: float = 0.5,
        eps: float = 0.95,
    ):
        self.env = gym.make(env)
        self.n_actions = n_actions
        self.n_states = n_states
        self.lr = lr
        self.df = df
        self.eps = eps

        self.Q = np.zeros((self.n_states, self.n_actions))

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

                self.update_epoch_end()

                all_num_iters.append(num_iter)
                pbar.set_postfix(
                    num_iter=num_iter,
                    min_num_iter=min(all_num_iters),
                    max_num_iter=max(all_num_iters),
                )

                self.env.close()

    def save(self, output_path: str):
        """Save trained Agent in pickle format."""

        dirname = os.path.dirname(output_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)

        with open(output_path, "wb") as outp:
            pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load(cls, agent_path: str) -> QLearningAgent:
        """Load trained Agent from pickle file."""

        with open(agent_path, "rb") as inp:
            agent: QLearningAgent = pickle.load(inp)

        return agent

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

    def update_epoch_end(self):
        """Update greedy epsilon."""

        self.eps *= self.eps

    def update_Q(self, action, current_state: int, next_state: int, reward: int):
        """Update Q matrix."""

        self.Q[current_state, action] += self.lr * (
            reward
            + self.df * (self.Q[next_state].max())
            - self.Q[current_state, action]
        )

    def __call__(self, state: int) -> int:
        n = np.random.uniform(0, 1)
        if n < self.eps:
            return self.env.action_space.sample()
        return int(np.argmax(self.Q[state]))


def main():
    """Main function."""

    agent = QLearningAgent(env=TAXI, n_actions=6, n_states=500, lr=LR, df=DF)

    output_file = "output/random_taxi.pkl"

    agent.fit(N_EPISODES)
    agent.save(output_file)

    agent_loaded = QLearningAgent.load(output_file)
    print(type(agent_loaded))
    agent_loaded.test()


if __name__ == "__main__":
    main()
