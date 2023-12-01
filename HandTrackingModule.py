import mediapipe as mp
import cv2
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2,modelC=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelC,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    #It searches for hands in the frame, and produces landmarks that trace their movement
    def findHands(self, frame, draw=True):

        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #Processes the hands and returns the landmarks
        results = self.hands.process(imgRGB)

        #in results the multi_hand_landmarks field contains the ID and
        #position of the landmarks found by the hands.process function
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if draw:
                    # Draw the landmarks
                    self.mpDraw.draw_landmarks(frame, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return frame

    #Saves the spatial positions of the landmarks and returns a list that
    #associates the positions of the landmarks over time with each id
    def findPosition(self, frame, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):

                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(frame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList


def main():
    # FrameRate var
    pTime = 0
    cTime = 0

    # init the camera
    cap = cv2.VideoCapture(0)

    detector = handDetector(detectionCon=0.5)
    while True:
        # get the current frame
        success, frame = cap.read()

        frame = cv2.flip(frame, 1)

        frame = detector.findHands(frame)

        lmList= detector.findPosition(frame)
        if len(lmList) != 0:
            #the indices of the landmarks are shown in the Documentation folder
            print(lmList[4])

        #Calculates and shows the framerate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Frame", frame)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()