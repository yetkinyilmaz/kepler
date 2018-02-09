import numpy as np
import pandas as pd


class AstroData(object):

    def __init__(self):
        self.depth = 3
        pass

    def convert(self, data):
        df = pd.DataFrame()
        for i in np.arange(0, self.depth):
            df[('t-' + str(i))] = data['position'].shift(i)
        return df.tail(len(df.index) - self.depth)
