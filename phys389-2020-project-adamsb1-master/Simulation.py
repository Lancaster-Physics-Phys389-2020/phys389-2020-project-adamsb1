import math
import numpy as np 
from Particle import Particle
from Pendulum2 import Pendulum
import scipy.constants
import matplotlib.pyplot as plt
import pandas as pd 
import copy

deltaT = 0.001
T = 0
endT = 10
                    # position          velocity        acceleration name   mass    theta          length  OMEGA    alpha E KE PE, damping factor
pend_ball_current = Pendulum(np.array([-4.,-0.5,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, scipy.constants.pi/2, 1., [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], 0.0, 0.0, 0.0, 0.0 )
total_data = []

update_method = 2                #1-euler, 2-cromer

while T <= endT:
    T += deltaT
    pend_ball_current.update(deltaT, update_method)
    pend_ball = copy.deepcopy(pend_ball_current)
    total_data.append([pend_ball.mass, pend_ball.position ,pend_ball.velocity ,pend_ball.acceleration, pend_ball.angle, pend_ball.length, pend_ball.ang_velocity, pend_ball.ang_acceleration, T,  pend_ball.tot_energy, pend_ball.kin_energy, pend_ball.pot_energy, pend_ball.damping_factor ])


#plt.plot(TIME, POSITION )
#plt.show()

df = pd.DataFrame(data = total_data, columns = ['mass','position','velocity','acceleration','angle','length','angular_velocity','angular_acceleration', 'time', 'tot_energy', 'kin_energy', 'pot_energy', 'damping_factor'])
#print(df['mass'][3])
df.to_pickle('Euler_update_c.csv')
print('done')