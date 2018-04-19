import numpy as np


class FeatureExtractor(object):

    def __init__(self):
        pass

    def transform(self, X_ds):
        self.n_sample = 15
        """Compute the El Nino mean at time t - (12 - X_ds.n_lookahead).

        Corresponding the month to be predicted.
        """
        # This is the range for which features should be provided. Strip
        # the burn-in from the beginning.
#        valid_range = np.arange(X_ds.n_burn_in, len(X_ds['time']))
        valid_range = np.arange(0, len(X_ds['time']))
        # Reshape into a matrix of one column
        X_array = X_ds['phi'].loc[:][valid_range].values.reshape(-1, 1)
        X_ts = np.ndarray(shape=(len(X_array), 0))
        for shift in np.arange(self.n_sample):
            X_ts = np.concatenate((X_ts, np.roll(X_array, shift)), axis=1)

        print("-------------------")
        print("Features: ", X_ts)
        print("Features shape: ", X_ts.shape)

        return X_ts
