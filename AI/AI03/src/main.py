from agents import RandomAgent

TAXI = "Taxi-v3"
CARTPOLE = "CartPole-v0"
LR = 1.0
DF = 0.5
N_EPISODES = 5_000


def main():
    """Main function."""

    agent = RandomAgent(TAXI, LR, DF)

    agent.fit(N_EPISODES)
    agent.test()


if __name__ == "__main__":
    main()
