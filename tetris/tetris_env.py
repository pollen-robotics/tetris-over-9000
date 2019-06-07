import gym
import numpy as np

from .core import Tetris, params

brick_size = 35
colors = {
    1: (149, 0, 237),
    2: (238, 0, 0),
    3: (0, 238, 0),
    4: (0, 0, 238),
    5: (238, 149, 0),
    6: (0, 238, 238),
    7: (238, 238, 0),
}


class TetrisEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
    }

    actions = [
        'none',
        'left', 'right',
        'cw', 'ccw',
        'drop',
    ]

    def __init__(self, drop_period=5):
        gym.Env.__init__(self)

        self.observation_space = gym.spaces.Box(
            low=0, high=8, shape=(params.n_rows, params.n_cols, 1),
            dtype=np.uint8
        )
        self.action_space = gym.spaces.Discrete(len(TetrisEnv.actions))

        self.game = Tetris()

        self.last_drop = 0
        self.drop_period = drop_period

        self.viewer = None

    def reset(self):
        self.game.reset()
        self.last_drop = 0

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

        if not self.game.done:
            self.last_drop += 1
            if self.last_drop > self.drop_period:
                self.game.drop()
                self.last_drop = 0
        else:
            self.last_drop = 0

        return self.game.state, 1, self.game.done, {}

    def render(self, mode='human'):
        from gym.envs.classic_control import rendering
        if self.viewer is None:
            self.viewer = rendering.Viewer(
                brick_size * params.n_cols,
                brick_size * params.n_rows
            )

        cur_state = self.game.state.copy()

        for y in range(params.n_rows):
            for x in range(params.n_cols):
                brick_id = cur_state[y, x, 0]
                if brick_id != 0:
                    top = ((params.n_rows - 1) - y) * brick_size
                    left = x * brick_size

                    path = [
                        (left, top),
                        (left + brick_size, top),
                        (left + brick_size, top + brick_size),
                        (left, top + brick_size)
                    ]
                    self.viewer.draw_polygon(path, color=colors[brick_id])

        return self.viewer.render(return_rgb_array=(mode == 'rgb_array'))
