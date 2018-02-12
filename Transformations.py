import numpy as np
import pandas as pd


def make_time_series_df(data, depth=10, label='position'):
    df = pd.DataFrame()
    for i in np.arange(0, depth):
        df[('t-' + str(i))] = data[label].shift(i)
    return df.tail(len(df.index) - depth)


def make_time_series(data, depth=2):
    n = len(data) - depth
    series = np.ndarray(shape=(n, 0))
    for i in np.arange(0, depth):
        series = np.hstack((series, data[i:n + i].reshape(-1, 1)))
    return series


def get_rho_phi(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)


def cylindrical(x_in):
    rho = np.zeros(len(x_in))
    phi = np.zeros(len(x_in))
    z = np.zeros(len(x_in))

    for i, v_car in enumerate(x_in):
        x_car, y_car, z_car = v_car[0], v_car[1], v_car[2]
        rho[i], phi[i] = get_rho_phi(x_car, y_car)
        z[i] = z_car
    v = np.dstack((rho, phi, z))[0]
    return v


def cartesian(x_in):
    x = np.zeros(len(x_in))
    y = np.zeros(len(x_in))
    z = np.zeros(len(x_in))

    for i, v_car in enumerate(x):
        x[i], y[i], z[i] = v_car[0], v_car[1], v_car[2]

    v = np.dstack((x, y, z))[0]
    return v
