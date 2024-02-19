import os
import HandTrackingModule as HTM
import numpy as np
import cv2


#path for exported data
DATA_PATH = os.path.join('MP_data')

#Action to collect
actions = np.array(['Minimize', 'Next', 'Previous', 'ScrollDown', 'ScrollUp', 'Volume'])

#Lenght of sequence to record the action
no_sequences = 30
sequence_lenght = 30

# Folder start
start_folder = 30

for action in actions:

    for sequence in range(0,no_sequences):
        try:
            os.makedirs(os.path.join(DATA_PATH, action, str(sequence)))
        except:
            pass

cap = cv2.VideoCapture(0)

detector =  HTM.handDetector(detectionCon=0.5)

while cap.isOpened():

    # Create the folder to collects and separates the data
    for action in actions:
        for sequence in range(no_sequences):
            for frame_num in range(sequence_lenght):

                #Get the current frame
                success, frame = cap.read()

                frame = cv2.flip(frame, 1)

                frame = detector.findHands(frame)

                if frame_num == 0:
                    cv2.putText(frame, 'STARTING COLLECTION', (120, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                    cv2.putText(frame, 'Collecting frame for {} Video Number {}'.format(action, sequence), (15, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 4, cv2.LINE_AA)
                    cv2.imshow('OpenCV Feed', frame)
                    cv2.waitKey(2000)
                else:
                    cv2.putText(frame, 'Collecting frame for {} Video Number {}'.format(action, sequence), (15, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 4, cv2.LINE_AA)



                lmList = detector.findPosition(frame)
                npy_path = os.path.join(DATA_PATH, action, str(sequence), str(frame_num))
                np.save(npy_path, lmList)

                cv2.imshow("Frame", frame)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

    cap.release()
    cv2.destroyAllWindows()

cap.release()
cv2.destroyAllWindows()