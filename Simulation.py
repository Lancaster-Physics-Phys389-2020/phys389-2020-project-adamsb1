import math
import numpy as np 
from Particle import Particle
from Pendulum import Pendulum
import scipy.constants
import matplotlib.pyplot as plt
import pandas as pd 

deltaT = 0.01
T = 0
endT = 50

pend_ball = Pendulum(np.array([1,1]),np.array([0,0]),np.array([0,0]),'ball', 1, scipy.constants.pi/2, 1., 0., 0. )
total_data = []
while T <= endT:
    T += deltaT
    pend_ball.update(deltaT)
    total_data.append([pend_ball.mass, pend_ball.position ,pend_ball.velocity ,pend_ball.acceleration, pend_ball.theta, pend_ball.length, pend_ball.omega, pend_ball.alpha, T ])


#plt.plot(TIME, POSITION )
#plt.show()

df = pd.DataFrame(data = total_data, columns = ['mass','position','velocity','acceleration','theta','length','omega','alpha', 'time'])
print(df['mass'][3])

df.plot(x = 'time', y = 'omega', kind = 'scatter')
plt.show()