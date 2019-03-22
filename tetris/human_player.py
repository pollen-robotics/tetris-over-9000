import pyglet
import pyglet.gl as gl

from .core import Tetris
from .render import brick_size, draw
from .arcade_stick import Arcade2PWrapper


if __name__ == '__main__':
    tetris = Tetris()
    rows, cols = tetris.state.shape

    width, height = cols * brick_size, rows * brick_size
    window = pyglet.window.Window(width, height, resizable=True, vsync=True)
    scale = [1]

    @window.event
    def on_draw():
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        draw(tetris.state, scale[0])

    @window.event
    def on_resize(w, h):
        scale[0] = h / height

    joysticks = pyglet.input.get_joysticks()
    joystick = joysticks[0]
    joystick.open()

    class MyController(object):
        def __init__(self, joystick):
            self.wrapper = Arcade2PWrapper(self, joystick)
            # joystick.push_handlers(self)
            self.action = None

        def on_joybutton_press(self, player, button):
            if button == 1:
                self.action = 'ccw'
            elif button == 0:
                self.action = 'cw'

        def on_joybutton_release(self, player, button):
            self.action = None

        def on_joyhat_motion(self, player, hat_x, hat_y):
            hat = (hat_x, hat_y)

            if hat == (0, 0):
                self.action = None
            elif hat == (-1, 0):
                self.action = 'left'
            elif hat == (1, 0):
                self.action = 'right'
            elif hat == (0, -1):
                self.action = 'down'

    c = MyController(joystick)

    def play(dt):
        if c.action == 'left':
            tetris.translate_piece(-1)
        elif c.action == 'right':
            tetris.translate_piece(1)
        elif c.action == 'down':
            tetris.drop()
        elif c.action == 'cw':
            tetris.rotate_piece(clockwise=True)
        elif c.action == 'ccw':
            tetris.rotate_piece(clockwise=False)

    apm = 1 / 10

    pyglet.clock.schedule_interval(play, apm)

    def drop(dt):
        tetris.drop()
        drop_rate = 1 / (tetris.nb_lines + 1)
        pyglet.clock.schedule_once(drop, drop_rate)
    pyglet.clock.schedule_once(drop, 1)

    pyglet.app.run()
