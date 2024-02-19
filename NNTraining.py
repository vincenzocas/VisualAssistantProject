from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import TensorBoard
import os
import DataCollection as dc
import LabelsCreationModule as lb

log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir = log_dir)

model = Sequential()
#30 is the frame's number, 63 is the number of values, 3 for each hand landmarks (x, y , z)
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30, 63)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu '))
model.add(Dense(32, activator= 'relu'))
#the last layer gives us an array of probability whose sum is 1
model.add(Dense(dc.actions.shape[0], activation='softmax'))

#Model Compile
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

model.fit(lb.X_train, lb.y_train, epochs = 2000, callbacks=[tb_callback])

#Model save
#model.save('TrainedModel.h5')