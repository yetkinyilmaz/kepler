
from Generate import *

sys = System()


for s in range(0,2):
    a = 80.
    v = 0.1
    position = a*np.random.random(2)
    velocity = v*np.random.random(2)
    data = sys.generate(position,velocity)
    data.to_csv("test.csv")






