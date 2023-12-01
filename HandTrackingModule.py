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

    def findHands(self, frame, draw=True):

        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # processa le mani e ritorna le landmarks
        results = self.hands.process(imgRGB)

        #in results il campo multi_hand_landmarks contiene id e posizione dei landmark trovati dalla funzione hands.process
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if draw:
                    # Disegna i landmarks
                    self.mpDraw.draw_landmarks(frame, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return frame


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