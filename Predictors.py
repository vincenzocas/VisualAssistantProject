from keras.models import Sequential
import numpy as np

import cv2
from keras.src.layers import LSTM, Dense

import HandTrackingModule as ht

actions = np.array(['Minimize', 'Next', 'Previous', 'ScrollDown', 'ScrollUp'])

colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245)]

def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85 + num * 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                    cv2.LINE_AA)
    return output_frame


model = Sequential()
# 30 is the frame's number, 63 is the number of values, 3 for each hand landmark 21 * (x, y , z)
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30, 63)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
# the last layer gives us an array of probability whose sum is 1
model.add(Dense(actions.shape[0], activation='softmax'))

# Model Compile
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])


model.load_weights('TrainedModel.h5')

#Detection vaiables

sequence = []
sentence = []
predictions = []
threshold = 0.4



# init the camera
cap = cv2.VideoCapture(0)

detector = ht.handDetector(detectionCon=0.5)
while True:
    # get the current frame
    success, frame = cap.read()

    frame = cv2.flip(frame, 1)

    frame = detector.findHands(frame)

    lmList = detector.findPosition(frame)

    #Prediction logic
    sequence.append( lmList)
    sequence = sequence[-30:]

    if len(sequence) == 30:
        res = model.predict(np.expand_dims(sequence, axis=0))[0]
        print(actions[np.argmax(res)])
        predictions.append(np.argmax(res))

    #Visualization
    if np.unique(predictions[-10:])[0] == np.argmax(res):
        if res[np.argmax(res)] > threshold:
            # if there are words in sentence, and check if the current prediction
            #isn't the same, in this case doesn't append to prevent duplication
            if len(sentence) > 0:
                if actions[np.argmax(res)] != sentence[-1]:
                    sentence.append(actions[np.argmax(res)])
            #if there aren't words in sentence, append
            else:
                sentence.append(actions[np.argmax(res)])


    if len(sentence) > 5:
        sentence = sentence[-5:]

    #Viz probabilities
    image = prob_viz(res, actions, frame, colors)

    cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
    cv2.putText(image, ' '.join(sentence), (3, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Frame", frame)
    # added functionality to close when pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()