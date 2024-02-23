import mouse
from pynput.keyboard import Key, Controller


scrollSpeed = 1

def scrollDown():
    mouse.wheel(-scrollSpeed)
    pass


def scrollUp():
    mouse.wheel(scrollSpeed)
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
