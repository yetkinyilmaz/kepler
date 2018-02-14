import numpy as np
import pandas as pd
from Transformations import *


class Body(object):

    def __init__(self, x=[], vx=[], m=1., r=0.00001, lum=1.):

        self.history = pd.DataFrame()
        self.position = [0., 0., 0.]
        self.momentum = [0., 0., 0.]

        self.mass = m
        self.radius = r
        self.luminosity = lum

        self.position[0] = x[0]
        self.position[1] = x[1]

        self.momentum[0] = vx[0]
        self.momentum[1] = vx[1]

    def update(self, acceleration, time):
        self.momentum += acceleration
        self.position += self.momentum
        self.history = self.history.append(pd.DataFrame(
            {'t': [time],
             'position': [self.position.copy()]}
        ), ignore_index=True)


# -------------------------------------------------------


class System(object):
    def __init__(self, n_steps=100):
        self.n_steps = n_steps
        self.bodies = np.array([])

    def force(self, position):
        g = 1.
        acc = -g * np.array(position) / \
            pow(np.linalg.norm(np.array(position)), 3)
        return acc

    def add_body(self, x=[], v=[], m=0):
        print("New body")
        p = Body(x, v, m)

        for t in range(0, self.n_steps):
            acceleration = self.force(p.position)
            p.update(acceleration, t)
#            if(t % 10 == 0):
#                print t, p.position

        self.bodies = np.append(self.bodies, p)

    def view(self, iref=0, n_res=1):
        reference = self.bodies[iref].history['position'].values
        n_body = len(self.bodies)
        self.cartesian = np.zeros(shape=n_body, dtype=object)
        self.cartesian_relative = np.zeros(shape=n_body, dtype=object)
        self.cylindrical_relative = np.zeros(shape=n_body, dtype=object)
        for i, p in enumerate(self.bodies):
            self.cartesian[i] = cartesian(p.history['position'].values)[::n_res]
            self.cartesian_relative[i] = cartesian(
                p.history['position'].values - reference)[::n_res]
            self.cylindrical_relative[i] = cylindrical(
                self.cartesian_relative[i])

    def generate(self, n):
        self.add_body(x=[60., 62.], v=[0.07, -0.06])
        self.add_body(x=[70., 73.], v=[0.07, -0.07])
