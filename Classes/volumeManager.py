import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import win32con
import win32api
import time

class VolumeManager:
    volume_levels = 1  # (speed)
    volume_delta = 0.015 * volume_levels  # approx. #volume_levels points in percent

    def __init__(self, videoCapId: int = 0):
        # init data to access the speakers
        self.cap = None
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        # self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)

        # init data for video capture
        if videoCapId is None:
            videoCapId = 0
        
        self.videoCapId = videoCapId
        # init detector
        self.detector = htm.handDetector(detectionCon=0.7)


    def raise_volume(self):

        win32api.keybd_event(win32con.VK_VOLUME_UP, 0)
        win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP)
        pass

    def lower_volume(self):

        win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0)
        win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, win32con.KEYEVENTF_KEYUP)
        #self.change_volume(t)
        pass

    def captureChangeVolume(self):
        """
        this function will be called to change the volume of the computer
        :return:
        """
        pTime = 0
        x1, x2, y1, y2 = 0, 0, 0, 0
        noHandCounter = 0
        self.cap = cv2.VideoCapture(self.videoCapId)
        while True:
            success, img = self.cap.read()
            # flip for preference
            # img = cv2.flip(img, 1)

            img = self.detector.findHands(img)

            # get landmark list
            lmList = self.detector.findPositionNoFlat(img, draw=False)

            if len(lmList) > 1:
                noHandCounter = 0
                # print(lmList[4], lmList[8])
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]

                xB, yB = lmList[0][1], lmList[0][2]
                xB2, yB2 = lmList[5][1], lmList[5][2]

                lengthBase = math.hypot(xB2 - xB, yB2 - yB)

                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                color = (255, 0, 255)

                length = math.hypot(x2 - x1, y2 - y1)
                # print(lengthBase, length, length/lengthBase)

                # less than the lower bound for the threshold
                if length < lengthBase * 0.15 or length < 25:
                    color = (0, 255, 0)
                    self.lower_volume()

                # more than the upper bound
                elif length > lengthBase * 1.3:
                    color = (255, 0, 0)
                    self.raise_volume()

                # cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                # cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                # cv2.circle(img, (cx, cy), 15, color, cv2.FILLED)

                pass
            else:
                if noHandCounter == 0:
                    noHandCounter = time.time()
                handTime = time.time()
                # time in seconds for it to close automatically
                if handTime - noHandCounter >= 2.5:
                    break

            # calc frame rate
            # cTime = time.time()
            # fps = 1 / (cTime - pTime)
            # pTime = cTime
            #
            # cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
            #
            # # display
            # cv2.imshow("", img)

            key = cv2.waitKey(1) & 0xFF

            # if key == ord('q'):
            #     break
            # pass
        self.cap.release()
        cv2.destroyAllWindows()
        pass

    pass
