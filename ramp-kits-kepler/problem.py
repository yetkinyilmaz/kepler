import os
import pandas as pd
import numpy as np
import rampwf as rw
import xarray as xr


problem_title =\
    'Prediction of the azimuth of Mars'

_n_lookahead = 1
_n_burn_in = 10  # approximately one year
_n_test = 5  # approximately ten years
_filename = 'test_angles_array.csv'
_target = 'phi'
# Need better error messages for invalid input parameters


Predictions = rw.prediction_types.make_regression(
    label_names=[_target])

# El Nino, a.k.a. [TimeSeries, FeatureExtractor, Regressor]
workflow = rw.workflows.ElNino(check_sizes=[132], check_indexs=[13])

score_types = [
    rw.score_types.RelativeRMSE(name='rel_rmse', precision=3)
]

# CV implemented here:
cv = rw.cvs.TimeSeries(
    n_cv=1, cv_block_size=0.1, period=2, unit='space_year')
get_cv = cv.get_cv

# Both train and test targets are stripped off the first
# n_burn_in entries


def _read_data(path):
    data_df = pd.read_csv(os.path.join(path, 'data', _filename))
    data_array = data_df.drop(['time'], axis=1).values[_n_lookahead:].reshape(-1)

    print("data_array: ", data_array)
    variables = data_df.columns.drop(['time']).values
    time = data_df['time'].values[_n_lookahead:]

    print("time : ", time)
    data_xr = xr.DataArray(
        data_array, coords=[('time', time)], dims=('time'))
    data_ds = xr.Dataset({'phi': data_xr})
    data_ds.attrs = {'n_burn_in': _n_burn_in}
    y_array = data_df[_target][:-_n_lookahead].values
    print("data_ds: ", data_ds)
    print("y_array: ", y_array.shape)

    return data_ds, y_array


def get_train_data(path='.'):
    data_ds, y_array = _read_data(path)
    data_ds = data_ds.isel(time=slice(None, -_n_test))
    y_array = y_array[_n_burn_in:-_n_test]
    # print('train')
    # print(data_ds)
    # print(data_ds['time'][-1])
    # print(y_array.shape)
    return data_ds, y_array


def get_test_data(path='.'):
    data_ds, y_array = _read_data(path)
    data_ds = data_ds.isel(time=slice(-_n_test, None))
    y_array = y_array[-_n_test + _n_burn_in:]
    # print('test')
    # print(data_ds)
    # print(data_ds['time'][0])
    # print(y_array.shape)
    return data_ds, y_array
