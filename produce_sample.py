import numpy as np
import pandas as pd
import Generate as gen
from Transformations import make_time_series

n_sample = 10
n_sim = 200000
n_view = 10

n_steps = n_sim / n_view
n_future = 20

s = gen.System()
s.force = s.force_gravity
s.generate()
s.simulate(n_sim)
s.view(0, n_view)

# time steps
# t = np.arange(0, n_sim / n_view) * n_view
# phis = s.get_phi(1)
# pd.DataFrame({'phi': [phis]}).to_csv('test_angles_single.csv', index=False)

phis = s.get_phi(1)
time = np.arange(len(phis)) * n_steps
data = pd.DataFrame({'time': time, 'phi': phis})\
    .to_csv('test_angles_array.csv',
            columns=['time', 'phi'],
            index=False)

df = pd.read_csv("test_angles_array.csv")
phis = df['phi'].values.reshape(-1, 1)
print(df)

x, y = make_time_series(phis, n_sample)
#y = y[n_future:len(y)]
#x = x[0:len(y) - n_future]

data = pd.DataFrame({'x_0': x[:, 0, 0],
                     'x_1': x[:, 1, 0],
                     'x_2': x[:, 2, 0],
                     'x_3': x[:, 3, 0],
                     'x_4': x[:, 4, 0],
                     'y_future': y})\
    .to_csv('test_series.csv',
            columns=['x_0', 'x_1', 'x_2', 'x_3', 'x_4', 'y_future'],
            index=False)





