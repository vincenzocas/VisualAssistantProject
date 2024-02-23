from keras.models import load_model
import numpy as np
from collections import deque, Counter

import cv2
from keras.src.layers import LSTM, Dense

import HandTrackingModule as ht

actions = np.array(['Minimize', 'Next', 'Previous', 'ScrollDown', 'ScrollUp'])

frame_threshold = 15

colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245), (116, 197, 205), (200, 100, 100)]


def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85 + num * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                    cv2.LINE_AA)
    return output_frame


def main():
    model = load_model("./../TrainedModel.h5")

    # Detection vaiables
    sequence = []
    sentence = []
    predictions = deque()
    threshold = 0.6
    # init the camera
    cap = cv2.VideoCapture(0)

    detector = ht.handDetector(detectionCon=0.75)
    while True:
        # get the current frame
        success, frame = cap.read()

        frame = cv2.flip(frame, 1)

        frame = detector.findHands(frame)

        lmList = detector.findPosition(frame)

        # print(np.shape(lmList))
        sequence = []
        sequence.append(lmList)

        # if len(sequence) == 30:
        res = model.predict(np.expand_dims(sequence, axis=0))[0]

        if np.argmax(res) > threshold:

            predictions.append(actions[np.argmax(res)])

            # # Viz probabilities # we only visualize if there is an action with more probability than the threshold
            frame = prob_viz(res, actions, frame, colors)

            # #after 15 frames of predictions it checks if there is one which occupied more than 12 frames
            if len(predictions) > frame_threshold:
                counter = Counter(predictions)
                # print(counter)
                predictions.clear()
                most = counter.most_common(1)[0]
                if most[1] >= frame_threshold * 0.8:
                    # #predicted action:
                    print(most[0])
                    pass
            pass
        pass
        
        cv2.imshow("Frame", frame)
        # added functionality to close when pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()