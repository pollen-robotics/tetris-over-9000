import pyglet


class Arcade2PWrapper(object):
    def __init__(self, delegate, joystick):
        self.delegate = delegate
        joystick.push_handlers(self)

        self.last_val = [(0, 0), (0, 0)]

        controls = joystick.device.get_controls()
        self.x1, self.x2 = controls[10], controls[-2]
        self.y1, self.y2 = controls[11], controls[-1]

    def on_joybutton_press(self, joystick, button):
        player_id = 1 if button < 10 else 2
        self.delegate.on_joybutton_press(player_id, button)

    def on_joybutton_release(self, joystick, button):
        player_id = 1 if button < 10 else 2
        self.delegate.on_joybutton_release(player_id, button)

    def val_to_hat(self, val):
        if val == -2:
            return -1
        return val

    def on_joyaxis_motion(self, joystick, axis, value):
        h1 = (self.val_to_hat(self.x1.value), -self.val_to_hat(self.y1.value))
        h2 = (self.val_to_hat(self.x2.value), -self.val_to_hat(self.y2.value))

        if self.last_val[0] != h1:
            self.delegate.on_joyhat_motion(1, *h1)
            self.last_val[0] = h1

        if self.last_val[1] != h2:
            self.delegate.on_joyhat_motion(2, *h2)
            self.last_val[1] = h2


if __name__ == '__main__':
    joysticks = pyglet.input.get_joysticks()
    joystick = joysticks[0]
    joystick.open()

    class MyController(object):
        def __init__(self, joystick):
            self.wrapper = Arcade2PWrapper(self, joystick)

        def on_joybutton_press(self, player, button):
            print('Player {} pressed button {}'.format(player, button))

        def on_joybutton_release(self, player, button):
            print('Player {} released button {}'.format(player, button))

        def on_joyhat_motion(self, player, hat_x, hat_y):
            print('Player {} moved hat to {}'.format(player, (hat_x, hat_y)))

    c = MyController(joystick)

    pyglet.app.run()
