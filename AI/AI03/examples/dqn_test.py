import gym
import torch
import torchvision.transforms as T
import numpy as np

JIT_PATH = "./output/dqn.pt"
DEVICE = "cpu"


def get_screen(env: gym.Env) -> torch.Tensor:
    """Get gym env render as RBG array."""

    render = env.render(mode="rgb_array").transpose((2, 0, 1))
    render = torch.from_numpy(render.astype(np.float32) / 255.0)
    render = render.unsqueeze(0)
    _, _, H, W = render.size()  # B, C, H, W
    render = T.functional.center_crop(render, (min(W, H), min(W, H)))
    render = T.functional.resize(render, (int(0.3 * min(W, H)), int(0.3 * min(W, H))))
    return render


def main():
    """Main function."""

    model = torch.jit.load(JIT_PATH)
    env = gym.make("CartPole-v1")

    env.reset()
    done = False

    last_screen = get_screen(env)
    current_screen = get_screen(env)
    s = (current_screen - last_screen).to(DEVICE)

    while not done:
        with torch.no_grad():
            a = torch.argmax(model(s), dim=1).item()
        _, _, done, *_ = env.step(a)

        last_screen = current_screen
        current_screen = get_screen(env)
        s = (current_screen - last_screen).to(DEVICE) if not done else None

        env.render()

    print("done!")

if __name__ == "__main__":
    main()
