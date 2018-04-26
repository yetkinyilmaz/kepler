from sklearn.base import BaseEstimator
from keras.layers import Input, Dense
from keras.models import Model
from keras.layers import LSTM
import numpy as np


class Regressor(BaseEstimator):
    def __init__(self):
        pass

    def fit(self, X, y):
        self.n_sample = X.shape[1]
        inputs = Input(shape=(self.n_sample, 1),
                       dtype='float', name='main_input')
        layer = LSTM(8)(inputs)
        predictions = Dense(1)(layer)
        self.model = Model(inputs=inputs, outputs=predictions)
        self.model.compile(optimizer='adam',
                           loss='mean_squared_error')

        self.model.fit(X.reshape(-1, self.n_sample, 1), y,
                       epochs=1, batch_size=1, verbose=2)
        print("I did something with fit")

    def predict(self, X):
        y_pred = np.array(self.model.predict(
            X.reshape(-1, self.n_sample, 1))).reshape(-1, 1)
        print("I did something with predict")

        return y_pred


class Regressor2(BaseEstimator):
    def __init__(self):
        pass

    def fit(self, X, y):
        self.n_sample = X.shape[1]
        inputs = Input(shape=(self.n_sample,),
                       dtype='float', name='main_input')
        layer = Dense(60,
                      activation='relu', kernel_initializer='normal')(inputs)
        layer = Dense(15,
                      activation='relu', kernel_initializer='normal')(layer)
        predictions = Dense(1,
                            kernel_initializer='normal')(layer)
        self.model = Model(inputs=inputs, outputs=predictions)
        self.model.compile(optimizer='adam',
                           loss='mean_squared_error')
        self.model.fit(X, y, epochs=5, batch_size=1, verbose=2)
        print("I did something with fit")

    def predict2(self, X):
        y_pred = np.array(self.model.predict(X)).reshape(-1, 1)
        print("I did something with predict")

        return y_pred
