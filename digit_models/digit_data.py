import pandas as pd
import numpy as np


def pad_arrays(array, longest):
    if len(array) < longest:
        filler = longest - len(array)
        filler_array = []
        for i in range(0, filler):
            zero_array = [0, 0, 0, 0, 0]
            filler_array.append(zero_array)
        return np.concatenate((array, filler_array), axis=0)
    else:
        return array


def class_array():
    driven_number = []

    for i in range(1, 10):
        if i != 2:
            for j in range(0, 32):
                driven_number.append(i)

    return driven_number


def read_data():
    movements = []
    for i in range(1, 10):
        if i != 2:
            for j in range(1, 33):
                data = pd.read_csv("./../data/digits/" + str(i) + "_" + str(j) + ".txt", header=None)
                movement = data.values
                movements.append(movement)

    longest_array = len(max(movements, key=len))

    new_movements = []
    for i in movements:
        new_movements.append(pad_arrays(i, longest_array))

    new_new_movements = []

    for i in new_movements:
        condensed_movement = []
        for n in range(0, 5):
            counter = 1
            new_value = 0
            for j in i:
                new_value += j[n]
                counter += 1
            new_value = new_value / counter
            condensed_movement.append(new_value)
        new_new_movements.append(condensed_movement)

    return pd.DataFrame(new_new_movements)


