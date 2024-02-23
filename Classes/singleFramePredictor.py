from keras.models import load_model
import numpy as np
from collections import deque, Counter

import cv2
from keras.src.layers import LSTM, Dense
from NNTraining import actions

import HandTrackingModule as ht

frame_threshold = 15
frame_width = 1280
frame_height = 720

colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245), (116, 197, 205), (200, 100, 100)]


def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), colors[num % len(colors)], -1)
        if prob >0.5:
            cv2.putText(output_frame, f"{actions[num]} {round(prob * 100, 2)}%", (0, 85 + num * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                    cv2.LINE_AA)
        else:
          cv2.putText(output_frame, f"{actions[num]}  ", (0, 85 + num * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                    cv2.LINE_AA)

    return output_frame




def take_command(folder: str = "./../TrainedModel.h5"):

    model = load_model(folder)

    # Detection vaiables
    sequence = []
    sentence = []
    predictions = deque()
    threshold = 0.6
    # init the camera
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    detector = ht.handDetector(detectionCon=0.75)
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
        frame = prob_viz(res, actions, frame, colors)
        if np.argmax(res) > threshold:

            predictions.append(actions[np.argmax(res)])

            # # Viz probabilities # we only visualize if there is an action with more probability than the threshold


            # #after 15 frames of predictions it checks if there is one which occupied more than 12 frames
            if len(predictions) > frame_threshold:

                counter = Counter(predictions)
                predictions.clear()

                most = counter.most_common(1)[0]
                # # most = (name , #of occurrences)
                if most[1] >= frame_threshold * 0.8:
                    # #predicted action:
                    # cap.release()
                    # cv2.destroyAllWindows()
                    # return most[0]
                    pass
            pass
        pass

        cv2.imshow("Frame", frame)
        # # added functionality to close when pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return None


if __name__ == "__main__":
    take_command()
