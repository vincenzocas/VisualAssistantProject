import numpy as np
import os


def get_sequences(directoryPath=''):
    get_sequences_var = os.listdir(directoryPath)
    j = []
    for i in range(len(get_sequences_var)):
        if os.path.isdir(os.path.join(directoryPath, get_sequences_var[i])):
            j.append(get_sequences_var[i])

    return j


if __name__ == '__main__':
    label_map = {}
    working_sequences, labels = [], []
    DATA_PATH = os.path.join('MP_data')
    list_actions = os.listdir(DATA_PATH)
    # zerosArray = np.zeros((63))
    for action in list_actions:
        print(action)
        dirPath = os.path.join(DATA_PATH, action, )
        # add action to label_map if it didn't exist beforehand
        label_map.setdefault(action, len(label_map.values()))
        sequences = get_sequences(dirPath)
        # print(len(sequences))
        for sequence in sequences:
            window = []
            frames = os.listdir(os.path.join(dirPath, sequence))
            # print( f" { len(frames)}")
            for frame in os.listdir(os.path.join(dirPath, sequence)):
                file = os.path.join(dirPath, sequence, frame)
                # print(file)
                if os.path.isfile(file):
                    res = np.load(file)
                    if len(res) != 63:
                        xs, ys, zs = [], [], []
                        for i in res:
                            xs.append(i[0])
                            ys.append(i[1])
                            zs.append(i[2])
                            pass

                        newArray = []
                        for x in xs:
                            newArray.append(x)
                        for y in ys:
                            newArray.append(y)
                        for z in zs:
                            newArray.append(z)

                        np.save(file, newArray)
                        # np.save(file, zerosArray)
                        pass


