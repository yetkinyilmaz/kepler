import numpy as np
from Transformations import *


class Body(object):

    def __init__(self, x=[], vx=[], i=0, m=1., r=0.00001, lum=1.):

        self.id = i
        self.history = np.ndarray(shape=(0, 3))
        self.position = np.array([0., 0., 0.])
        self.momentum = np.array([0., 0., 0.])

        self.mass = m
        self.radius = r
        self.luminosity = lum

        self.position[0] = x[0]
        self.position[1] = x[1]

        self.momentum[0] = vx[0]
        self.momentum[1] = vx[1]

    def update(self, acceleration):
        self.momentum += acceleration
        self.position += self.momentum
        self.history = np.concatenate(
            (self.history, self.position.reshape(1, -1)))

# -------------------------------------------------------


class System(object):
    def __init__(self):
        self.n_steps = 0
        self.bodies = np.array([])

    def force_single_sun(self, p):
        g = 1.
        acc = -g * np.array(p.position) / \
            pow(np.linalg.norm(p.position), 3)
        return acc

    def force_double_sun(self, p):
        g = 1.
        acc = np.array([0., 0., 0.])
        suns = [np.array([-50., 0., 0.]),
                np.array([50., 0., 0.])]
        for sun in suns:
            acc += -g * np.array(p.position - sun) / \
                pow(np.linalg.norm(p.position - sun), 3)
        return acc

    def force_gravity(self, p):
        g = 1.
        acc = np.array([0., 0., 0.])

        for body in self.bodies:
            if(p.id != body.id):
                acc += -g * body.mass * \
                    np.array(p.position - body.position) / \
                    pow(np.linalg.norm(p.position - body.position), 3)
        return acc

    def add_body(self, x=[], v=[], i=0, m=0):
        p = Body(x, v, i, m)
        self.bodies = np.append(self.bodies, p)

    def view(self, iref=0, n_res=1):
        reference = self.bodies[iref].history
        n_body = len(self.bodies)
        self.cartesian = np.zeros(shape=n_body, dtype=object)
        self.cartesian_relative = np.zeros(shape=n_body, dtype=object)
        self.cylindrical_relative = np.zeros(shape=n_body, dtype=object)
        for i, p in enumerate(self.bodies):
            self.cartesian[i] = cartesian(
                p.history)[::n_res]
            self.cartesian_relative[i] = cartesian(
                p.history - reference)[::n_res]
            self.cylindrical_relative[i] = cylindrical(
                self.cartesian_relative[i])

    def generate(self, n):
        self.add_body(x=[60., 62.], v=[0.07, -0.06], i=0, m=0.000001)
        self.add_body(x=[70., 73.], v=[0.07, -0.07], i=1, m=0.000001)
        self.add_body(x=[74., 76.], v=[0.075, -0.075], i=2, m=0.000001)
        self.add_body(x=[174., 176.], v=[0.025, -0.035], i=3, m=0.000001)
        self.add_body(x=[0., 0.], v=[0., 0.], i=4, m=1.)

    def simulate(self, n_steps):
        for t in np.arange(0, n_steps):
            for p in self.bodies:
                acceleration = self.force(p)
                p.update(acceleration)
        self.n_steps += n_steps
