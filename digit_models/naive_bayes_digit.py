from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from digit_models import digit_data

driven_number = digit_data.class_array()
data_movement = digit_data.read_data()

X = data_movement
print(X)
y = driven_number

X_train, X_test, y_train, y_test = train_test_split(X, y)

gnb = GaussianNB()

gnb.fit(X_train, y_train)

predictions = gnb.predict(X_test)

print(predictions)

print(gnb.score(X_test, y_test))

print(classification_report(y_test, predictions))

# gnb = GaussianNB()
# y_pred = gnb.fit(data_movement, driven_number).predict(data_movement)
#
# print("Number of mislabeled points out of a total %d points : %d" % (len(driven_number),(driven_number != y_pred).sum()))