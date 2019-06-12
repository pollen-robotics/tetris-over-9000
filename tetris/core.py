import numpy as np

from . import params
from .piece import Piece


class Tetris(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = np.zeros((params.n_rows, params.n_cols), dtype=np.uint8)
        self.piece = Piece.generate_random_new()
        self.nb_lines = 0
        self.nb_piece = 1
        self.done = False

    def translate_piece(self, dx):
        new_x = self.piece.x + dx

        if not self.check_collision(self.piece, (new_x, self.piece.y)):
            self.piece.x = new_x

    def rotate_piece(self, clockwise):
        rotated_piece = Piece.rotate(self.piece, clockwise)
        if not self.check_collision(rotated_piece, rotated_piece.pos):
            self.piece = rotated_piece

    def drop(self):
        new_y = self.piece.y + 1

        if not self.check_collision(self.piece, (self.piece.x, new_y)):
            self.piece.y = new_y

        else:
            self.merge_piece_to_board()
            self.check_and_remove_full_lines()

            self.piece = Piece.generate_random_new()
            self.nb_piece += 1

            if self.check_collision(self.piece, self.piece.pos):
                self.reset()
                self.done = True

    @property
    def state(self):
        state = self.board.copy()

        lx, rx, ly, ry = self.piece.get_range_at(self.piece.pos)
        state[ly:ry, lx:rx] += self.piece.shape

        return np.expand_dims(state, axis=-1)

    def check_collision(self, piece, pos):
        lx, rx, ly, ry = piece.get_range_at(pos)
        if (lx < 0 or rx > self.board.shape[1]) or (ly < 0 or ry > self.board.shape[0]):
            return True
        return np.bitwise_and(
            self.board[ly:ry, lx:rx] != 0,
            piece.shape != 0
        ).any()

    def merge_piece_to_board(self):
        lx, rx, ly, ry = self.piece.get_range_at(self.piece.pos)
        self.board[ly:ry, lx:rx] += self.piece.shape

    def check_and_remove_full_lines(self):
        complete_line_indexes = np.where(self.board.all(axis=1))[0]

        self.board = np.vstack((
            np.zeros((len(complete_line_indexes), params.n_cols), dtype=np.uint8),
            np.delete(self.board, complete_line_indexes, axis=0),
        ))

        self.nb_lines += len(complete_line_indexes)
