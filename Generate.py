import numpy as np
from Transformations import *


class Body(object):

    def __init__(self, x=[], vx=[], i=0, m=1., r=0.00001, lum=1., spring=1.):

        self.id = i
        self.history = np.ndarray(shape=(0, 3))
        self.position = np.array([0., 0., 0.])
        self.momentum = np.array([0., 0., 0.])

        self.mass = m
        self.radius = r
        self.luminosity = lum

        self.spring = spring
        self.position[0] = x[0]
        self.position[1] = x[1]

        self.momentum[0] = m * vx[0]
        self.momentum[1] = m * vx[1]

    def update(self, force):
        self.momentum += force
        self.position += self.momentum / self.mass
        debug = False
        if(debug):
            print("position : ", self.position)
            print("momentum : ", self.momentum)
            print("force    : ", force)

        self.history = np.concatenate(
            (self.history, self.position.reshape(1, -1)))

# -------------------------------------------------------


class System(object):
    def __init__(self):
        self.n_steps = 0
        self.bodies = np.array([])
        self.g = 1.
        self.k = 1.
        self.f = 1.

    def get_phi(self, i):
        return np.copy(self.cylindrical_relative[i][:, 1])

    def force_single_sun(self, p):
        force = -self.g * p.mass * p.position / \
            pow(np.linalg.norm(p.position), 3)
        return force

    def force_double_sun(self, p):
        force = np.array([0., 0., 0.])
        suns = [np.array([-50., 0., 0.]),
                np.array([50., 0., 0.])]
        for sun in suns:
            rel_pos = p.position - sun.position
            force += -self.g * p.mass * rel_pos / \
                pow(np.linalg.norm(rel_pos), 3)
        return force

    def force_gravity(self, p):
        force = np.array([0., 0., 0.])

        for body in self.bodies:
            if(p.id != body.id):
                rel_pos = p.position - body.position
                force += -self.g * p.mass * body.mass * \
                    rel_pos / \
                    pow(np.linalg.norm(rel_pos), 3)
        return force

    def force_spring(self, p):
        force = np.array([0., 0., 0.])
        if(p.id > 0):
            for body in self.bodies:
                if(np.abs(p.id - body.id) == 1):
                    spring = p.spring
                    if(body.id > p.id):
                        spring = body.spring
                    rel_pos = p.position - body.position
                    dist = np.linalg.norm(rel_pos)
                    stretch = np.abs(dist - spring)
                    if(stretch > 0.):
                        if(stretch < (spring * 0.9)):
                            force += -self.k * rel_pos *  \
                                stretch / dist
                    if(False):
                        print("planet : ----------", p.id)
                        print("body : ----------", body.id)
                        print("dist:", dist)
                        print("spring:", spring)
                        print("stretch:", stretch)
                        print("force:", force)
        return force

    def force_constant_y(self, p):
        force = p.mass * np.array([0., self.f, 0])
        return force

    def force_pendulum_spring(self, p):
        force = np.array([0., 0., 0.])
        if(p.id > 0):
            force = self.force_spring(p) + self.force_constant_y(p)
        return force

    def tension_pendulum(self, p, force_ext=np.array([0., 0., 0.])):
        tension = np.array([0., 0., 0.])
        force_long = np.array([0., 0., 0.])
        if(p.id > 0):
            body = self.bodies[p.id - 1]
            rel_pos = p.position - body.position
            norm = np.linalg.norm(rel_pos)
#                    print("norm : ", norm)
            centripetal = np.dot(p.momentum, p.momentum) \
                / p.mass / norm
            force_long = np.dot(rel_pos, force_ext) / norm
            stre = centripetal + force_long
            tension -= rel_pos * stre / norm
#           force = force_ext + tension
#            print("tension : ", tension, "  gravity : ", gravity)
        return tension

    def add_body(self, x=[], v=[], m=0., stretch=0.):

        position = np.array(x)
        velocity = np.array(v)

        while(len(position) < 3):
            position = np.append(position, 0.)
        while(len(velocity) < 3):
            velocity = np.append(velocity, 0.)

        spring = 0.
        i = len(self.bodies)
        if(len(self.bodies) > 0):
            rel_pos = position - self.bodies[i - 1].position
            spring = np.linalg.norm(rel_pos) + stretch
        print("Adding body with spring length : ", spring)
        p = Body(position, velocity, i, m, spring=spring)
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
        self.add_body(x=[60., 62.], v=[0.07, -0.06], m=0.000001)
        self.add_body(x=[70., 73.], v=[0.07, -0.07], m=0.000001)
        self.add_body(x=[74., 76.], v=[0.075, -0.075], m=0.000001)
        self.add_body(x=[174., 176.], v=[0.025, -0.035], m=0.000001)
        self.add_body(x=[0., 0.], v=[0., 0.], i=4, m=1.)

    def simulate(self, n_steps):
        for t in np.arange(0, n_steps):
            forces = np.ndarray(shape=(0, 3))
            for i, p in enumerate(self.bodies):
                forces = np.concatenate((forces, self.force(p).reshape(1, -1)))
            for i, p in enumerate(self.bodies):
                p.update(forces[i])
        self.n_steps += n_steps

    def simulate_pendulum(self, n_steps):
        for t in np.arange(0, n_steps):
            force_down = np.array([0., 0., 0.])
            for p in self.bodies[::-1]:
                gravity = self.force_constant_y(p)
                force_ext = gravity + force_down
                force_up = self.tension_pendulum(p, force_ext)
                force = force_down + force_up + gravity
                p.update(force)
                force_down += force_up
        self.n_steps += n_steps
