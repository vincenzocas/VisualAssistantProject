import sys

from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import numpy as np
import os
import DataCollection as Dc


label_map = {label: num for num, label in enumerate(Dc.action)}

sequences, labels = [], []
for action in Dc.action:
    for sequence in range(Dc.no_sequences):
        window = []
        for frame_num in range(Dc.sequence_lenght):
            res = np.load(os.path.join(Dc.DATA_PATH, Dc.action, str(sequence), "{}.npy".format(frame_num)))
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])


#print(np.array(sequences).shape)
#print(np.array(labels).shape)

X = np.array(sequences)
y = to_categorical(labels).astype(int)



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
#print(y_train.shape)