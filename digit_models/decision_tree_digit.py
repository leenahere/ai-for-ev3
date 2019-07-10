from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import tree
from digit_models import digit_data
import matplotlib.pyplot as plt

driven_number = digit_data.class_array()
data_movement = digit_data.read_data()

X = data_movement
y = driven_number

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = tree.DecisionTreeClassifier(splitter='best', max_depth=5)

model.fit(X_train, y_train)

plt.figure(figsize=(12.80,9.60))
tree.plot_tree(model.fit(X_train, y_train))
plt.show()

predictions = model.predict(X_test)

print(predictions)

print(model.score(X_test, y_test))

print(classification_report(y_test, predictions))