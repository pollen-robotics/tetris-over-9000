import operator
import numpy as np

from .core import params
from .tetris_env import TetrisEnv


class Bot(object):
    def __init__(self, env):
        self.env = env

        self.next_actions = []
        self.last_nb_piece = 0

    def predict(self, obs):
        if self.new_piece():
            self.next_actions = self.select_next_drop(obs)

        if not self.next_actions:
            return self.env.action_space.sample()
        return self.next_actions.pop()

    def new_piece(self):
        if self.env.game.nb_piece != self.last_nb_piece:
            self.last_nb_piece = self.env.game.nb_piece
            return True
        return False

    def select_next_drop(self, obs):
        poss = self.find_all_drop_possibilities()
        poss = {
            k: self.game_state_metrics(k, state)
            for (k, state) in poss.items()
        }

        best_drop = self.find_better_solution(poss)
        rot, col, n_drop, _ = best_drop

        dx = col - self.env.game.piece.x
        translate = 'left' if dx < 0 else 'right'

        actions = ['cw'] * rot + [translate] * abs(dx) + ['drop'] * n_drop
        actions = list(reversed(actions))

        return [TetrisEnv.actions.index(a) for a in actions]

    def find_all_drop_possibilities(self):
        poss = {}

        for rot in range(4):
            for col in range(params.n_cols):
                game = self.env.game.copy()
                game.nb_lines = 0

                for _ in range(rot):
                    game.rotate_piece(clockwise=True)

                y_dim = game.piece.shape.shape[1]
                if col + y_dim > params.n_cols:
                    continue
                game.piece.x = col

                n_drop = 0
                while True:
                    new_y = game.piece.y + 1
                    if game.check_collision(game.piece, (game.piece.x, new_y)):
                        break
                    game.piece.y = new_y
                    n_drop += 1

                poss[(rot, col, n_drop + 1, game.nb_lines)] = game.state

        return poss

    def find_better_solution(self, possibilities):
        def value(nb_lines, nb_holes, heights):
            aggregate_height = heights.sum()
            bumpiness = np.abs(np.diff(heights)).sum()

            a = -0.5
            b = 0.75
            c = -0.35
            d = -0.2

            return a * aggregate_height + b * nb_lines + c * nb_holes + d * bumpiness

        possibilities = {
            k: value(*v)
            for k, v in possibilities.items()
        }
        key, val = max(possibilities.items(), key=operator.itemgetter(1))
        return key

        # best_drop = list(possibilities.keys())[0]
        # best_val = (np.inf, np.inf, np.inf, np.inf)
        #
        # for drop, (nb_lines, nb_holes, heights) in possibilities.items():
        #     val = (-nb_lines, nb_holes, heights.max(), heights.mean())
        #     if val < best_val:
        #         best_val = val
        #         best_drop = drop
        #
        # return best_drop

    def game_state_metrics(self, key, state):
        _, _, _, nb_lines = key

        nb_holes = len(self.get_holes(state)[0])

        heights = self.state_height(state)

        return nb_lines, nb_holes, heights

    def state_height(self, state):
        mask = state[:, :, 0] != 0
        return params.n_rows - np.where(mask.any(axis=0), mask.argmax(axis=0), params.n_rows)

    def get_holes(self, state):
        brick_mask = np.zeros(self.env.game.state.shape, dtype=np.bool)
        for i, h in enumerate(self.state_height(state)):
            brick_mask[20 - h:, i] = True

        hole_mask = state == 0
        return np.where(np.bitwise_and(hole_mask, brick_mask))
