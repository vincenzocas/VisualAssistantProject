from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import TensorBoard
import os
import LabelCreation2 as lb
import numpy as np

actions = np.array(['Minimize', 'Next', "Nothing", 'Previous', 'ScrollDown', 'ScrollUp', 'volume']) #,'Exit'])


def main():
    log_dir = os.path.join('Logs')
    tb_callback = TensorBoard(log_dir=log_dir)

    model = Sequential()
    # 30 is the frame's number, 63 is the number of values, 3 for each hand landmark 21 * (x, y , z)
    model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(1, 63)))
    model.add(LSTM(128, return_sequences=True, activation='relu'))
    model.add(LSTM(64, return_sequences=False, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    # the last layer gives us an array of probability whose sum is 1
    model.add(Dense(actions.shape[0], activation='softmax'))

    # Model Compile
    model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
    # init labeler
    labeler = lb.Labeler()
    model.fit(labeler.X_train, labeler.y_train, epochs=2000, callbacks=[tb_callback], validation_split=0.25,
              batch_size=20)

    # Model save
    model.save('TrainedModel.h5')
    pass


if __name__ == "__main__":
    main()
    pass
