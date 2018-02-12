import numpy as np
import pandas as pd


class Planet(object):

    def __init__(self, x=[], vx=[]):

        self.history = pd.DataFrame()
        self.position = [0., 0., 0.]
        self.momentum = [0., 0., 0.]

        self.position[0] = x[0]
        self.position[1] = x[1]

        self.momentum[0] = vx[0]
        self.momentum[1] = vx[1]
        #self.history = pd.DataFrame({'t': [22], 'position': [self.position]})

    def update(self, acceleration, time):
        self.momentum += acceleration
        self.position += self.momentum
        self.history = self.history.append(pd.DataFrame(
            {'t': [time],
             'position': [self.position.copy()]}
        ), ignore_index=True)


class System(object):
    def __init__(self, n_steps=100):
        self.n_steps = n_steps
        self.planets = np.array([])

    def force(self, position):
        g = 0.5
        acc = -g * np.array(position) / pow(np.linalg.norm(np.array(position)), 3)
        return acc

    def add_planet(self, x=[], v=[]):
        print("New planet")
        p = Planet(x, v)

        for t in range(0, self.n_steps):
            acceleration = self.force(p.position)
            p.update(acceleration, t)
#            if(t % 10 == 0):
#                print t, p.position

        self.planets = np.append(self.planets, p)
        return p.history

    def view():
        reference = self.planets[0].history['position'].values
        for i, p in enumerate(self.planets):
            for t, step in enumerate(p.history['position'].values):
                relative_position = step - reference

    def generate():
        self.add_planet(x=[20.,30.],v=[0.4,-0.6])
        self.add_planet(x=[10.,20.],v=[0.2,-0.7])


