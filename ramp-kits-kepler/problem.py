import os
import pandas as pd
import numpy as np
import rampwf as rw
from sklearn.model_selection import ShuffleSplit

problem_title =\
    'Prediction of the azimuth of Mars'

_target_column_name_reg = 'y_future'

Predictions = rw.prediction_types.make_regression(
    label_names=[_target_column_name_reg])
# The workflow object, named after the RAMP.
workflow = rw.workflows.Regressor()

score_types = [
    rw.score_types.RMSE(name='rmse', precision=3)
]


def _read_data(path, f_name):
    X_df = pd.read_csv(os.path.join(path, 'data', f_name))
    y_columns = [_target_column_name_reg]
    y_array = X_df[y_columns].values.reshape(-1, 1)
    X_df = X_df.drop(y_columns, axis=1)
    return X_df, y_array


def get_train_data(path='.'):
    f_name = 'train.csv.bz2'
    return _read_data(path, f_name)


def get_test_data(path='.'):
    f_name = 'test.csv.bz2'
    return _read_data(path, f_name)


def get_cv(X, y):
    cv = ShuffleSplit(n_splits=2, test_size=0.5, random_state=1)
    splits = cv.split(X)
    print(splits)

    # not having this print list crashes
#    something = list(splits)
    #  File "/anaconda/envs/python36/lib/python3.6/site-packages/rampwf/utils/testing.py", line 210, in assert_submission
    #    module_path, X_train, y_train, train_is=train_is)
    # adds \n between indices!

    return splits
