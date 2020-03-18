import math
import numpy as np 
from Particle import Particle
from Pendulum2 import Pendulum
from Double_Pendulum import DoublePendulum
import scipy.constants
import matplotlib.pyplot as plt
import pandas as pd 
import copy

deltaT = 0.001
T = 0
endT = 5

update_method = 4              #1-euler, 2-cromer, 3-richardson, 4 = RK



df = 0.00


                    # position          velocity        acceleration name   mass    theta          length  OMEGA    alpha  ORIGIN POINT E KE PE, damping factor
pendulum1 = np.array([np.array([-4.,-3.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, scipy.constants.pi/2, 1., [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], 0.0, 0.0, 0.0, df])
pendulum2 = np.array([np.array([-8.,-6.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 2, scipy.constants.pi/2, 1., [0.,0.,0.], [0.,0.,0.], [-4.,-3.,0.], 0.0, 0.0, 0.0, df])

listofobjects = [pendulum1, pendulum2]
#pend_ball_current = pendulum1
total_data1 = []
total_data2 = []

pendulums = DoublePendulum(listofobjects)
pendulums.run_simulation(endT, deltaT, update_method)

#
#x=0
#while T <= endT:
#    T += deltaT
#    pendulums = [pendulum1, pendulum2]
 #   for i in range(0, len(pendulums)):
#        pendulums[i].update(deltaT, update_method)
#    pendulums_data = copy.deepcopy(pendulums)

#    i = 0
#    while i < 2:
#        if i == 0:
#            total_data1.append([pendulums_data[i].mass, pendulums_data[i].position ,pendulums_data[i].velocity ,pendulums_data[i].acceleration, pendulums_data[i].angle, pendulums_data[i].length, pendulums_data[i].ang_velocity, pendulums_data[i].ang_acceleration, T,  pendulums_data[i].tot_energy, pendulums_data[i].kin_energy, pendulums_data[i].pot_energy, pendulums_data[i].damping_factor ])
#        elif i == 1:
#            total_data2.append([pendulums_data[i].mass, pendulums_data[i].position ,pendulums_data[i].velocity ,pendulums_data[i].acceleration, pendulums_data[i].angle, pendulums_data[i].length, pendulums_data[i].ang_velocity, pendulums_data[i].ang_acceleration, T,  pendulums_data[i].tot_energy, pendulums_data[i].kin_energy, pendulums_data[i].pot_energy, pendulums_data[i].damping_factor ])
#        i+=1

#    if x == 100:
#        print(T)
#        x=0
#    x+=1
#plt.plot(TIME, POSITION )
#plt.show()


#df = pd.DataFrame(data = total_data1, columns = ['mass','position','velocity','acceleration','angle','length','angular_velocity','angular_acceleration', 'time', 'tot_energy', 'kin_energy', 'pot_energy', 'damping_factor'])
#df.to_pickle('Pendulum_RK_1.csv')

#df = pd.DataFrame(data = total_data2, columns = ['mass','position','velocity','acceleration','angle','length','angular_velocity','angular_acceleration', 'time', 'tot_energy', 'kin_energy', 'pot_energy', 'damping_factor'])
#df.to_pickle('Pendulum_RK_2.csv')

#print('done')
