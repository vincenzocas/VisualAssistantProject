import mouse
from pynput.keyboard import Key, Controller


def scrollDown():
    mouse.wheel(-1)
    pass


def scrollUp():
    mouse.wheel(1)
    pass


class KeyPressManager:

    def __init__(self):
        self.keyboard = Controller()
        pass

    def lastPage(self):
        self.keyboard.press(Key.ctrl_l)
        self.keyboard.press(Key.left)
        self.keyboard.release(Key.left)
        self.keyboard.release(Key.ctrl_l)
        pass

    def nextPage(self):
        self.keyboard.press(Key.ctrl_l)
        self.keyboard.press(Key.right)
        self.keyboard.release(Key.right)
        self.keyboard.release(Key.ctrl_l)
        pass
