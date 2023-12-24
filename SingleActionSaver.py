import logging
import os
import argparse
import sys
import string
import random

import HandTrackingModule as HTM
import numpy as np
import cv2

DATA_PATH = os.path.join('MP_data')


def get_random_string(length=8):
    # choose from all lowercase letter
    letters = string.ascii_uppercase
    letters.join(string.digits)

    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


if __name__ == '__main__':
    # arg parser
    parser = argparse.ArgumentParser(description="Program which will save an action for NN testing.\n"
                                                 "Will make you repeat the action in front of your camera a "
                                                 "certain number of times to have training data.\n")

    # parameters for parser
    parser.add_argument("action_name", help="Name/Label of the action to be saved.", default=None)
    parser.add_argument("-r", "--repetitions",
                        help="Number of repetitions to be saved.\n",
                        default=30, type=int, nargs=1)
    parser.add_argument("-t", "--time",
                        help="Length of time the action should take in number of frames.Min 10, Max 30\n",
                        default=30, type=int, nargs=1,
                        choices=range(10, 31))
    parser.add_argument("-o", dest="output",
                        help="Base name of the output directories where the data will be saved."
                             " It will override any preexisting directory with the same name if there are any.\n",
                        default=None, type=str)
    # parse args
    args = parser.parse_args()

    action_name = args.action_name
    if args.output:
        output = args.output
    else:
        output = get_random_string(10)

        while os.path.isdir(os.path.join(DATA_PATH, action_name, f"{output}_0")):
            output = get_random_string(10)

    working_path = os.path.join(DATA_PATH, action_name, output)

    repetitions = args.repetitions
    frames = args.time

    # title of window
    title = f"Action capturer: {action_name}"

    # starting variables
    iteration = 0
    cap = cv2.VideoCapture(0)
    detector = HTM.handDetector(detectionCon=0.5)
    capturing = False
    frame_n = 0

    while cap.isOpened():
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = detector.findHands(frame)
        key = cv2.waitKey(1) & 0xFF

        if capturing:
            # Frame text
            frame_n += 1
            cv2.putText(frame, f'Collecting frame for {action_name} Video Number {iteration}/{repetitions}',
                        (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Frame {frame_n}/{frames}',
                        (int(len(frame[0]) * 0.8), 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            # detecting hands
            lmList = detector.findPosition(frame)

            # check if the directory exists, if it doesn't create it
            if not os.path.isdir(os.path.join(DATA_PATH, action_name, f"{output}_{iteration}")):
                os.makedirs(os.path.join(DATA_PATH, action_name, f"{output}_{iteration}"))

            npy_path = os.path.join(DATA_PATH, action_name, f"{output}_{iteration}", str(frame_n))

            np.save(npy_path, lmList)

            if frame_n == args.time:
                capturing = False
                iteration += 1
            pass

        else:  # when not capturing

            cv2.putText(frame, f'Press \"C\" when ready for next capture\n'
                               f'Press \"Q\" to Exit', (15, 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            if key == ord('c'):
                frame_n = 0
                capturing = True
            elif key == ord('q'):
                break
            pass

        if iteration >= repetitions:
            print("Finished all iterations.\n")
            break

        cv2.imshow(title, frame)
        pass
    cap.release()
    cv2.destroyAllWindows()
    pass
