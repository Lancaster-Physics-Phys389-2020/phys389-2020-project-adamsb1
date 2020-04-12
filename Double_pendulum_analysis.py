import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp
'''
This file creates all the analysis plots for the double pendulum system.
'''

###########
#Import data files using Pandas
pen_1 = pd.read_pickle(r'Pendulum_testing_06_04.csv')
pen_2 = pd.read_pickle(r'Pendulum_testing2_06_04.csv')
time_analysis = pd.read_pickle(r'Pendulum_time_analysis_06_04.csv')
###########


###########
#Plot of total energy against time for the double pendulum system.
print(pen_1['time'])
plt.figure(figsize = [8.0,8.0])
plt.plot(  [pen_1['time'][i] for i in range(len(pen_1['time']))],  [pen_1['tot_energy'][i] + pen_2['tot_energy'][i]  for i in range(len(pen_1['tot_energy']))], 'red')
plt.ylabel('Total Energy [J]', size =20)
plt.xlabel('Time [s]', size =20)
plt.savefig('DP_energy_2.pdf')
plt.close()
###########

###########
#Analysis of time-taken-to-flip

x1 = np.zeros([144])
x2 =np.zeros([144])
y1=np.zeros([144])
y2=np.zeros([144])      #Creates a set of numpy arrays to store data in during analysis
phi1=np.zeros([144])
phi2=np.zeros([144])
time = np.zeros([144])
ang1 = []
ang2 = []
time_final = []


#####
#Data selection
for i in range(len(time_analysis['initial_pend1'])):
    x1[i] = time_analysis['initial_pend1'][i][0]
    y1[i] = time_analysis['initial_pend1'][i][1]
    x2[i] = (time_analysis['initial_pend2'][i][0] - time_analysis['initial_pend1'][i][0] )     #Finds initial position of each pendulum relative to it's origin point
    y2[i] = (time_analysis['initial_pend2'][i][1] - time_analysis['initial_pend1'][i][1] )
    time = time_analysis['time_to_flip']

    phi1[i] = (np.arctan2(y1[i],x1[i]) + (sp.pi/2))
    if phi1[i]> sp.pi:
        phi1[i] = phi1[i] -sp.pi * 2.                       #Converts inital position to polar angle
    phi2[i] = (np.arctan2(y2[i],x2[i]) + (sp.pi/2))         #Also ensures: -pi < phi < pi
    if phi2[i]> sp.pi:
        phi2[i] = phi2[i] -sp.pi * 2. 


    if time[i] != 'no flip':        #Cuts data down to only include initial conditions that caused teh pendulum to flip
        ang1.append(phi1[i])
        ang2.append(phi2[i])
        time_final.append(time[i])
#####

#####
#Plotting data as scatter with energy consideration curves.
plt.figure(figsize = [8.0,8.0])
plt.scatter(ang1 ,ang2, s = 12, c = time_final, cmap='plasma')
plt.ylabel('Top pendulum angle [rad]', size =16, )
plt.xlabel('Bottom pendulum angle [rad]', size =16)

y = np.arange(-3.,3.,0.1)
x = np.arccos( (2. - np.cos(y))/ 3.)
x2= - x                                 #Energy consideration curve
plt.plot(x,y, 'k')
plt.plot(x2,y, 'k')

plt.colorbar()
plt.savefig('time_2d_15.pdf')
plt.close()
#####

###########


