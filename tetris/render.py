import os
import pyglet

import tetris

asset_folder = os.path.join(os.path.dirname(tetris.__file__), 'assets')
id2color = {
    1: 'yellow',
    2: 'yellow',
    3: 'yellow',
    4: 'yellow',
    5: 'yellow',
    6: 'yellow',
    7: 'yellow',
}
bricks = {
    color: pyglet.image.load(os.path.join(asset_folder, 'brick.png'))
    for color in id2color.values()
}
brick_size = 35


def draw(tetris_state, scale):
    batch = pyglet.graphics.Batch()

    rows, cols = tetris_state.shape

    sprites = []

    for y in range(rows):
        for x in range(cols):
            pixel = tetris_state[y, x]
            if pixel:
                img = bricks[id2color[pixel]]

                py = ((rows - 1) - y) * (brick_size * scale)
                px = x * (brick_size * scale)

                s = pyglet.sprite.Sprite(img, x=px, y=py, batch=batch)
                s.update(scale=scale)
                sprites.append(s)

    batch.draw()


if __name__ == '__main__':
    import pyglet.gl as gl
    import numpy as np

    from .core import Tetris

    tetris = Tetris()
    rows, cols = tetris.state.shape

    width, height = cols * brick_size, rows * brick_size
    window = pyglet.window.Window(width, height, resizable=True, vsync=True)

    def play():
        actions = ('left', 'right', 'cw', 'ccw', 'drop')
        a = np.random.choice(actions)
        if a == 'left':
            tetris.translate_piece(-1)
        elif a == 'right':
            tetris.translate_piece(1)
        if a == 'cw':
            tetris.rotate_piece(clockwise=True)
        elif a == 'ccw':
            tetris.rotate_piece(clockwise=False)
        else:
            tetris.drop()

    @window.event
    def on_draw():
        play()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        draw(tetris.state)

    def dummy(dt):
        pass

    pyglet.clock.schedule_interval(dummy, 1 / 30)
    pyglet.app.run()
