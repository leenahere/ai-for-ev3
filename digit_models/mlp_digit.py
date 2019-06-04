from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
import pickle
from digit_models import digit_data

driven_number = digit_data.class_array()
data_movement = digit_data.read_data()

X = data_movement
print(X)
y = driven_number

X_train, X_test, y_train, y_test = train_test_split(X, y)

print(X_train)

scaler = StandardScaler()
scaler.fit(X_train)

pickle.dump(scaler, open('mlp_scaler.pkl', 'wb'))

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

mlp = MLPClassifier(hidden_layer_sizes=(13,13,13),max_iter=500)
mlp.fit(X_train,y_train)

file = 'trained_model.sav'
pickle.dump(mlp, open(file, 'wb'))

predictions = mlp.predict(X_test)
print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
