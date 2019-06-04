from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.svm import SVC
from digit_models import digit_data

driven_number = digit_data.class_array()
data_movement = digit_data.read_data()

X = data_movement
print(X)
y = driven_number

X_train, X_test, y_train, y_test = train_test_split(X, y)

sv_classifier = SVC(kernel='poly', degree=8)
sv_classifier.fit(X_train, y_train)

y_pred = sv_classifier.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))