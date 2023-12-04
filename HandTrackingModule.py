import mediapipe as mp
import cv2
import time
import os
from matplotlib import pyplot as plt
import numpy as np

class handDetector():
    def __init__(self, mode=False, maxHands=2, modelC=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelC,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    # It searches for hands in the frame, and produces landmarks that trace their movement
    def findHands(self, frame, draw=True):

        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgRGB.flags.writeable = False
        # Processes the hands and returns the landmarks
        self.results = self.hands.process(imgRGB)

        imgRGB.flags.writeable = True
        # in results the multi_hand_landmarks field contains the ID and
        # position of the landmarks found by the hands.process function
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # Draw the landmarks
                    self.mpDraw.draw_landmarks(frame, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return frame

    # Saves the spatial positions of the landmarks and returns a list that
    # associates the positions of the landmarks over time with each id
    def findPosition(self, frame, handNo=0, draw=False):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):

                h, w, c = frame.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), lm.z
                test = np.array([id, cx, cy, cz]).flatten()
                lmList.append(test)
        else: lmList.append(np.zeros(21*3)) #if there aren't data to collect fill the list with 0 matrix

        print(lmList)
        np.save('0', lmList)
        np.load('0.npy')
        return lmList

    def collect_data(self, lmList):
        np.save('0', lmList)
        np.load('0.npy')



def main():
    # FrameRate var
    pTime = 0
    cTime = 0

    # init the camera
    cap = cv2.VideoCapture(0)

    detector =  handDetector(detectionCon=0.5)
    while True:
        # get the current frame
        success, frame = cap.read()

        frame = cv2.flip(frame, 1)

        frame = detector.findHands(frame)

        lmList = detector.findPosition(frame)


        # Calculates and shows the framerate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Frame", frame)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
