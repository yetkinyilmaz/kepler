import numpy as np
import pandas as pd


class Planet(object):

    def __init__(self, x = [], vx = []):

        self.history = pd.DataFrame()
        self.position = np.zeros(3);
        self.momentum = np.zeros(3);

        self.position[0] = x[0]
        self.position[1] = x[1]

        self.momentum[0] = vx[0]
        self.momentum[1] = vx[1]

        history = pd.DataFrame({'t':[22], 'position':[self.position]})
        print history

        pass

    def update(self,acceleration, time):
        self.momentum += acceleration;
        self.position += self.momentum;
        self.history = self.history.append(pd.DataFrame({'t':[time], 'position':[self.position.copy()]}), ignore_index=True)
        pass


class System(object):
    def __init__(self):
        pass

    def force(self,position):
        g = 0.5
        acc = -g * position / pow(np.linalg.norm(position),3)
        return acc


    def generate(self,x=[], vx=[]):
        print "New planet"
        p = Planet(x,vx)

        for t in range(0,100):
            acceleration = self.force(p.position)
            p.update(acceleration, t)
#            if(t % 10 == 0):
#                print t, p.position

        return p.history



#s = System()

#print s.generate(50.0, 0.0, 0.02,0.05)
#s.generate(30.0, 0.0, 0.02,0.05)
#s.generate(30.0, 10.0, 0.02,0.05)
#s.generate(30.0, 15.0, 0.02,0.05)

