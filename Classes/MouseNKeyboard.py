import mouse
from pynput.keyboard import Key, Controller
import numpy as np
from keras.models import load_model
from collections import deque
import cv2
from NNTraining import actions
import HandTrackingModule as ht

frame_threshold = 3
import DefaulBrowserDetect as db

scrollSpeed = 1

def scrollDown():
    mouse.wheel(-scrollSpeed)
    pass


def scrollUp():
    mouse.wheel(scrollSpeed)
    pass


def scroll(model):
    # Detection vaiables
    sequence = []
    sentence = []
    predictions = deque()
    threshold = 0.75
    # init the camera
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    detector = ht.handDetector(detectionCon=0.75)
    timer = 0

    while True:
        # get the current frame
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame)
        # print(np.shape(lmList))
        sequence = [lmList]

        # if len(sequence) == 30:
        res = model.predict(np.expand_dims(sequence, axis=0))[0]
        # frame = prob_viz(res, actions, frame, colors)
        if np.argmax(res) > threshold:
            # #after 15 frames of predictions it checks if there is one which occupied more than 12 frames
            if len(predictions) > frame_threshold:
                if actions[np.argmax(res)] == "scrollUp":
                    timer = 0
                    scrollUp()
                    pass
                elif actions[np.argmax(res)] == "scrollDown":
                    timer = 0
                    scrollDown()
                    pass
                else:
                    timer += 1
                    pass
            pass
        pass

        # cv2.imshow("Frame", frame)
        # # added functionality to close when pressing 'q'
        if timer >= 30:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
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

        
if __name__ == "__main__":
    model = load_model("./../TrainedModel.h5")
    scroll(model)
    pass