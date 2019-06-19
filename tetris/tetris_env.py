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

    available_rewards = (
        'lines completed',  # number of lines cleared by previous action
        'new pieces',  # +1 if a new piece appeared else 0
        'each step',  # +1 at each time step
        'matris',  # +1 per drop + 100 * (nb lines ** 2)
    )

    def __init__(self, rewards, drop_period=5):
        gym.Env.__init__(self)

        self.observation_space = gym.spaces.Box(
            low=0, high=8, shape=(params.n_rows, params.n_cols, 1),
            dtype=np.uint8
        )
        self.action_space = gym.spaces.Discrete(len(TetrisEnv.actions))

        if rewards not in TetrisEnv.available_rewards:
            raise ValueError('rewards should be one of {}'.format(TetrisEnv.available_rewards))
        self.rewards = rewards

        self.game = Tetris()

        self.last_drop = 0
        self.drop_period = drop_period

        self.last_nb_piece = 0
        self.last_nb_line = 0

        self.viewer = None

    def reset(self):
        self.game.reset()
        self.last_drop = 0
        self.last_nb_piece = 0

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

        return self.game.state, self.compute_rewards(action), self.game.done, {}

    def compute_rewards(self, action):
        cleared_lines = max(self.game.nb_lines - self.last_nb_line, 0)

        if self.rewards == 'lines completed':
            reward = cleared_lines
        elif self.rewards == 'new pieces':
            reward = 1 if self.last_nb_piece != self.game.nb_piece else 0
        elif self.rewards == 'each step':
            reward = 1
        elif self.rewards == 'matris':
            reward = 1 if action == 'drop' else 0
            reward += 100 * cleared_lines ** 2

        self.last_nb_piece = self.game.nb_piece
        self.last_nb_line = self.game.nb_lines

        return reward

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
