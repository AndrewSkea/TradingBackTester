import numpy
import pandas
import time
import datetime
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
import numpy

# fix random seed for reproducibility
numpy.random.seed(7)

# load dataset
dataframe = pandas.read_csv("results_2_norm.csv", header=None)
dataset = dataframe.values
X = dataset[:, 0:4].astype(float)
Y = dataset[:, 6]

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

model = Sequential()
model.add(Dense(8, input_dim=4, activation='sigmoid'))
# model.add(Dense(8, activation='relu'))
model.add(Dense(3, activation='sigmoid'))
# Compile model
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X, dummy_y, epochs=500, batch_size=300, verbose=2)
# evaluate the model
scores = model.evaluate(X, dummy_y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# calculate predictions
# predictions = model.predict(X)
# # round predictions
# rounded = [round(x[0]) for x in predictions]
# print(rounded)





#
#
# def baseline_model():
#     # create model
#     model = Sequential()
#     model.add(Dense(5, input_dim=6, activation="relu", kernel_initializer="uniform"))
#     model.add(Dense(3, activation="softmax"))
#     # Compile model
#     model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
#     # print(model.get_weights())
#     return model
#
#
# time_now = time.time()
# estimator = KerasClassifier(build_fn=baseline_model, epochs=10, batch_size=10, verbose=2)
# kfold = KFold(n_splits=3, shuffle=False)
# results = cross_val_score(estimator, X, dummy_y, cv=kfold)
#
# file = open('final_result.txt', 'a')
#
# string1 = ("Accuracy: %.2f%% (%.2f%%)\n" % (results.mean() * 100, results.std() * 100))
# string2 = "Process took: {} seconds\n\n".format(str(datetime.timedelta(seconds=time.time() - time_now)))
#
# print(string1)
# print(string2)
#
# file.write(string1)
# file.write(string2)
