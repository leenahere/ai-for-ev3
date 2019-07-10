from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from digit_models import digit_data

driven_number = digit_data.class_array()
data_movement = digit_data.read_data()

X = data_movement
print(X)
y = driven_number

X_train, X_test, y_train, y_test = train_test_split(X, y)

logmodel = LogisticRegression(multi_class='auto', solver='newton-cg')

logmodel.fit(X_train, y_train)

predictions = logmodel.predict(X_test)

print(predictions)

print(logmodel.score(X_test, y_test))

print(classification_report(y_test, predictions))