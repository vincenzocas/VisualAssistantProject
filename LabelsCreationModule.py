from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import numpy as np
import os

#path for exported data
DATA_PATH = os.path.join('MP_data')

actions = np.array(['Activate'])

#Lenght of sequence to record the action
no_sequences = 30
sequence_lenght = 30

label_map = {label: num for num, label in enumerate(actions)}

sequences, labels = [], []
for action in actions:
    for sequence in range(no_sequences):
        window = []
        for frame_num in range(sequence_lenght):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), "{}.npy".format(frame_num)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

#print(np.array(sequences).shape)
#print(np.array(labels).shape)

X = np.array(sequences)
y = to_categorical(labels).astype(int)



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
#print(y_train.shape)