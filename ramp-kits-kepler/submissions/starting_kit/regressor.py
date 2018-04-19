from sklearn.base import BaseEstimator
from keras.layers import Input, Dense
from keras.models import Model


class Regressor(BaseEstimator):
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

    def predict(self, X):
        y_pred = self.model.predict(X).reshape(-1, 1)
        return y_pred
