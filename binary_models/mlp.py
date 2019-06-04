import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix


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


movements = []
col_names = ['left', 'middle', 'right', 'motor_left', 'motor_right']

for i in range(1,16):
    data = pd.read_csv("./../data/binary_classification/circle_" + str(i) +".txt", names=col_names, header=None)
    movement = data.values
    movements.append(movement)
    data_s = pd.read_csv("./../data/binary_classification/square_" + str(i) +".txt", names=col_names, header=None)
    movement_s = data_s.values
    movements.append(movement_s)

longest_array = len(max(movements,key=len))

new_movements = []
for i in movements:
    new_movements.append(pad_arrays(i, longest_array))


new_new_movements = []

for i in new_movements:
    condensed_movement = []
    for n in range(0,5):
        counter = 1
        new_value = 0
        for j in i:
            new_value += j[n]
            counter += 1
        new_value = new_value / counter
        condensed_movement.append(new_value)
    new_new_movements.append(condensed_movement)


print(new_new_movements)
print(len(new_new_movements))

driven_number = np.array([0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1])

data_movement = pd.DataFrame(new_new_movements)
print(data_movement)

X = data_movement
print(X)
y = driven_number

X_train, X_test, y_train, y_test = train_test_split(X, y)

print(X_train)

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

mlp = MLPClassifier(hidden_layer_sizes=(13,13,13),max_iter=500)
mlp.fit(X_train,y_train)

predictions = mlp.predict(X_test)
print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
