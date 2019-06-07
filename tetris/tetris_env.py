import gym
import numpy as np

from .core import Tetris, params


class TetrisEnv(gym.Env):
    metadata = {
        'render.modes': ['human'],
    }

    actions = [
        'none',
        'left', 'right',
        'cw', 'ccw',
        'drop',
    ]

    def __init__(self, max_steps):
        self.observation_space = gym.spaces.Box(
            low=0, high=8, shape=(params.n_rows, params.n_cols),
            dtype=np.uint8
        )
        self.action_space = gym.spaces.Discrete(len(TetrisEnv.actions))

        self.game = Tetris()

    def reset(self):
        self.game.reset()
        return self.game.state

    def step(self, action):
        action = TetrisEnv.actions[action]

        if action == 'left':
            self.game.translate_piece(-1)
        elif action == 'right':
            self.game.translate_piece(1)
        elif action == 'cw':
            self.game.rotate_piece(clockwise=True)
        elif action == 'ccw':
            self.game.rotate_piece(clockwise=False)
        elif action == 'drop':
            self.game.drop()

        return self.game.state, 1, self.game.done, {}

    def render(self, mode='human'):
        # return True
        pass


gym.envs.registration.register(
    id='Tetris-v0',
    entry_point='tetris.tetris_env:TetrisEnv',
    max_episode_steps=9999999,
    reward_threshold=32000,
    kwargs={'max_steps': np.inf},
    nondeterministic=True,
)


if __name__ == '__main__':
    import gym
    import tetris.tetris_env

    env = gym.make('Tetris-v0')
    env.reset()

    done = False
    R = 0

    while not done:
        state, reward, done, _ = env.step(env.action_space.sample())
        R += reward
    print(R)