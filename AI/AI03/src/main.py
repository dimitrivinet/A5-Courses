from agents import RandomAgent

TAXI = "Taxi-v3"
CARTPOLE = "CartPole-v0"

LR = 1.0
DF = 0.5
N_EPISODES = 10_000


def main():
    """Main function."""

    agent = RandomAgent(env=TAXI, n_actions=6, n_states=500, lr=LR, df=DF)

    output_file = "output/random_taxi.pkl"

    agent.fit(N_EPISODES)
    agent.save(output_file)

    agent_loaded = RandomAgent.load(output_file)
    print(type(agent_loaded))
    agent_loaded.test()


if __name__ == "__main__":
    main()
