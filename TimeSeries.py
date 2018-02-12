import numpy as np
import pandas as pd


def make_time_series(self, data, depth=10, label='position'):
    df = pd.DataFrame()
    for i in np.arange(0, self.depth):
        df[('t-' + str(i))] = data[label].shift(i)
    return df.tail(len(df.index) - self.depth)


def cartesian_to_polar(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)
