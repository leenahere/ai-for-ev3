from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from digit_models import digit_data

driven_number = digit_data.class_array()
data_movement = digit_data.read_data()

X = data_movement
print(X)
y = driven_number

X_train, X_test, y_train, y_test = train_test_split(X, y)

# Create KNN classifier
knn = KNeighborsClassifier(n_neighbors = 2)
# Fit the classifier to the data
knn.fit(X_train,y_train)

#show predictions on the test data
print(knn.predict(X_test))

#check accuracy of our model on the test data
print(knn.score(X_test, y_test))