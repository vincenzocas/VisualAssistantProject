import mouse
from pynput.keyboard import Key, Controller
import DefaulBrowserDetect as db

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
        browser_id = db.get_default_browser_windows()
        if browser_id == "FirefoxURL":
            self.keyboard.press(Key.alt)
            self.keyboard.press(Key.left)
            self.keyboard.release(Key.left)
            self.keyboard.release(Key.alt)
            return
        elif browser_id == "ChromeHTML":
            self.keyboard.press(Key.alt)
            self.keyboard.press(Key.left)
            self.keyboard.release(Key.left)
            self.keyboard.release(Key.alt)
            return
        elif browser_id == "AppXq0fevzme2pys62n3e0fbqa7peapykr8v":
            self.keyboard.press(Key.alt)
            self.keyboard.press(Key.left)
            self.keyboard.release(Key.left)
            self.keyboard.release(Key.alt)
            return
        elif browser_id == "OperaStable":
            self.keyboard.press(Key.alt)
            self.keyboard.press(Key.left)
            self.keyboard.release(Key.left)
            self.keyboard.release(Key.alt)
            return
        else:
            return "Browser non riconosciuto"
        pass

    def nextPage(self):
        browser_id = db.get_default_browser_windows()
        if browser_id == "FirefoxURL":
            self.keyboard.press(Key.alt)
            self.keyboard.press(Key.right)
            self.keyboard.release(Key.right)
            self.keyboard.release(Key.alt)
            return
        elif browser_id == "ChromeHTML":
            self.keyboard.press(Key.alt)
            self.keyboard.press(Key.right)
            self.keyboard.release(Key.right)
            self.keyboard.release(Key.alt)
            return
        elif browser_id == "AppXq0fevzme2pys62n3e0fbqa7peapykr8v":
            self.keyboard.press(Key.alt)
            self.keyboard.press(Key.right)
            self.keyboard.release(Key.right)
            self.keyboard.release(Key.alt)
            return
        elif browser_id == "OperaStable":
            self.keyboard.press(Key.alt)
            self.keyboard.press(Key.right)
            self.keyboard.release(Key.right)
            self.keyboard.release(Key.alt)
            return
        else:
            return "Browser non riconosciuto"
        pass