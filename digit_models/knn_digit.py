from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from digit_models import digit_data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import ListedColormap
import seaborn as sns

#driven_number = digit_data.class_array()
#data_movement = digit_data.read_data()

#data_movement.columns = ['left_sensor', 'middle_sensor', 'right_sensor', 'left_motor', 'right_motor']
data = pd.read_csv("./../data.csv")
print(data)
driven_number = data["class"]
print(driven_number)
data_movement = data.copy()
data_movement = data_movement.drop("class", axis=1)


#data_for_plot = data_movement.copy()
#data_for_plot['class'] = driven_number
#print(data_for_plot)

pairplot = sns.pairplot(data, vars=['left_sensor', 'middle_sensor', 'right_sensor', 'left_motor_speed', 'right_motor_speed'], hue="class")
plt.show()
pairplot.savefig("pairplot.png")
print(data_movement)
#X = data_movement.iloc[:, 3:]
X = data_movement.to_numpy()
X = X[:, 3:]
print(X)
y = driven_number
print(y)

h = .02

c_map_dark = ListedColormap(['#f01d6a', '#000000', '#5a8f6f', '#aa8282', '#83adb5', '#2ecc71', '#f1c40f', '#9b59b6', '#03396c'])
c_map_light = ListedColormap(['#f78eb4', '#000000', '#a4dbba', '#f4baba', '#d9e6e8', '#d5f4e2', '#f9e79f', '#ebddf0', '#4e7498'])

X_train, X_test, y_train, y_test = train_test_split(X, y)

# Create KNN classifier
knn = KNeighborsClassifier(n_neighbors=2, metric="manhattan")
# Fit the classifier to the data
#knn.fit(X_train,y_train)
knn.fit(X,y)

x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])

Z = Z.reshape(xx.shape)

plt.figure()
plt.pcolormesh(xx, yy, Z, cmap=c_map_light)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=c_map_dark)
plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.show()


#show predictions on the test data
print(knn.predict(X_test))

#check accuracy of our model on the test data
print(knn.score(X_test, y_test))