import numpy as np

from . import params


class Piece(object):
    def __init__(self, shape, x, y):
        self.shape = shape
        self.x = x
        self.y = y

    @property
    def pos(self):
        return self.x, self.y

    @property
    def dim(self):
        return tuple(reversed(self.shape.shape))

    def get_range_at(self, pos):
        return pos[0], pos[0] + self.dim[0], pos[1], pos[1] + self.dim[1]

    @classmethod
    def generate_random_new(cls):
        shape = np.random.choice(shapes)
        return cls(shape, params.n_cols // 2 - shape.shape[1] // 2, 0)

    @classmethod
    def rotate(cls, piece, clockwise):
        shape = np.rot90(piece.shape, 1 if clockwise else 3)
        return cls(shape.copy(), piece.x, piece.y)


shapes = (
    np.array((
        (1, 1, 1),
        (0, 1, 0),
    ), dtype=np.uint8),
    np.array((
        (0, 2, 2),
        (2, 2, 0),
    ), dtype=np.uint8),
    np.array((
        (3, 3, 0),
        (0, 3, 3),
    ), dtype=np.uint8),
    np.array((
        (4, 0, 0),
        (4, 4, 4),
    ), dtype=np.uint8),
    np.array((
        (0, 0, 5),
        (5, 5, 5),
    ), dtype=np.uint8),
    np.array((
        (6, 6, 6, 6),
    ), dtype=np.uint8),
    np.array((
        (7, 7),
        (7, 7),
    ), dtype=np.uint8),
)
