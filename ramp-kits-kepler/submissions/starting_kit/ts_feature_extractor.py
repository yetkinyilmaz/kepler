import numpy as np


class FeatureExtractor(object):

    def __init__(self):
        pass

    def transform(self, X_ds):
        """Compute the El Nino mean at time t - (12 - X_ds.n_lookahead).

        Corresponding the month to be predicted.
        """
        # This is the range for which features should be provided. Strip
        # the burn-in from the beginning.
        valid_range = np.arange(X_ds.n_burn_in, len(X_ds['time']))

        # Reshape into a matrix of one column
        X_array = X_ds['phi'].loc[:][valid_range].values.reshape(-1, 1)
        print("-------------------")
        print("Features: ", X_array)
        return X_array
