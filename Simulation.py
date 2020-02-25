import math
import numpy as np 
from Particle import Particle
from Pendulum2 import Pendulum
import scipy.constants
import matplotlib.pyplot as plt
import pandas as pd 

deltaT = 0.001
T = 0
endT = 50
                    # position          velocity        acceleration name   mass    theta          length  OMEGA    alpha
pend_ball = Pendulum(np.array([3.,4.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, scipy.constants.pi/2, 1., [0.,0.,0.], [0.,0.,0.], [0.,0.,0.] )
total_data = []
while T <= endT:
    T += deltaT
    pend_ball.update(deltaT)
    total_data.append([pend_ball.mass, pend_ball.position ,pend_ball.velocity ,pend_ball.acceleration, pend_ball.angle, pend_ball.length, pend_ball.ang_velocity, pend_ball.ang_acceleration, T ])


#plt.plot(TIME, POSITION )
#plt.show()

df = pd.DataFrame(data = total_data, columns = ['mass','position','velocity','acceleration','theta','length','omega','alpha', 'time'])
print(df['mass'][3])

#df.plot(x = 'time', y = 'theta',y ='alpha', kind = 'scatter')
plt.plot(df['time'], df['theta'], 'red', label = 'theta')
plt.plot(df['time'], df['alpha'], 'blue', label = 'alpha')
plt.legend()
plt.show()