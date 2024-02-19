import os
import numpy as np
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split


def get_sequences(directoryPath=''):
    get_sequences_var = os.listdir(directoryPath)
    j = []
    for i in range(len(get_sequences_var)):
        if os.path.isdir(os.path.join(directoryPath, get_sequences_var[i])):
            j.append(get_sequences_var[i])

    return j


class Labeler:
    def __init__(self):
        label_map = {}
        working_sequences, labels = [], []
        DATA_PATH = os.path.join('MP_data')
        list_actions = os.listdir(DATA_PATH)

        for action in list_actions:
            dirPath = os.path.join(DATA_PATH, action, )
            print(action)
            # add action to label_map if it didn't exist beforehand
            label_map.setdefault(action, len(label_map.values()))
            sequences = get_sequences(dirPath)

            for sequence in sequences:
                window = []
                for frame in os.listdir(os.path.join(dirPath, sequence)):
                    file = os.path.join(dirPath, sequence, frame)

                    if os.path.isfile(file):
                        res = np.load(file)
                        window.append(res)
                if len(window) > 0:
                    working_sequences.append(window)
                    labels.append(label_map[action])

        x = np.asarray(working_sequences)
        y = to_categorical(labels).astype(int)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.05)
        pass
    pass
