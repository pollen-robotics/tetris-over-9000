import gym
import numpy as np

from .core import Tetris, params
from .tetris_env import TetrisEnv

class TetrisEnv2(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
    }

    def __init__(self, drop_period=5):
        gym.Env.__init__(self)

        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(params.n_rows, params.n_cols, 1),
            dtype=np.uint8
        )
        self.action_space = gym.spaces.Discrete(params.n_cols*4)

        self.game_env = TetrisEnv('new pieces')
        
    def reset(self):
        return self.game_env.reset()

    def step(self, action):
        next_actions = self.generate_actions_drop(action) 
        done = False
        while (next_actions) :
            next_a = next_actions.pop()
            state, rew, done, _ =  self.game_env.step(next_a)
            self.render()
            if (done or rew==1):
                break
        rew = self.reward()

        return self.game_env.game.state, rew, done, {}
    
    def render(self, mode='human'):
        return self.game_env.render(mode)

    def reward(self):
        nb_lines, nb_holes, heights = self.game_state_metrics(self.game_env.game.state)
        
        print(nb_lines, nb_holes, heights)
        aggregate_height = heights.sum()
        bumpiness = np.abs(np.diff(heights)).sum()
        a = -0.51
        b = 0.76
        c = -0.36
        d = -0.19
        return a * aggregate_height + b * nb_lines + c * nb_holes + d * bumpiness

    def game_state_metrics(self, state):
        nb_lines = self.game_env.game.nb_lines - self.game_env.last_nb_line
        nb_holes = len(self.get_holes(self.game_env.game.board)[0])
        heights = self.state_height(self.game_env.game.board)
        return nb_lines, nb_holes, heights

    def state_height(self, state):
        mask = state[:, :] != 0
        return params.n_rows - np.where(mask.any(axis=0), mask.argmax(axis=0), params.n_rows)

    def get_holes(self, state):
        brick_mask = np.zeros(self.game_env.game.board.shape, dtype=np.bool)
        for i, h in enumerate(self.state_height(state)):
            brick_mask[20 - h:, i] = True
        hole_mask = state == 0
        return np.where(np.bitwise_and(hole_mask, brick_mask))
    
    def generate_actions_drop(self, action):
        rot = action % 4
        col = (int) (action / 4)
        game = self.game_env.game.copy()
        game.nb_lines = 0
        for _ in range(rot):
            game.rotate_piece(clockwise=True)
            
        y_dim = game.piece.shape.shape[1]
        if col + y_dim > params.n_cols:
            col = params.n_cols - y_dim 
        game.piece.x = col
        
        n_drop = 0
        while True:
            new_y = game.piece.y + 1
            if game.check_collision(game.piece, (game.piece.x, new_y)):
                break
            game.piece.y = new_y
            n_drop += 1
            
        dx = col - self.game_env.game.piece.x
        translate = 'left' if dx < 0 else 'right'

        actions = ['cw'] * rot + [translate] * abs(dx) + ['drop'] * (n_drop+1)
        actions = list(reversed(actions))
        return [TetrisEnv.actions.index(a) for a in actions]