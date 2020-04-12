import math
import numpy as np 
from Particle import Particle
from Pendulum2 import Pendulum
from Double_Pendulum import DoublePendulum
import scipy.constants
import pandas as pd 
import copy
'''
This file is used to set the initial condidtions of the system, including all data for the pendulums, time-step size, duration of the simulation, update method and damping factor.
This file also allows single pendulum analysis as well as double pendulum time and energy analysis.
It also saves the data from the simulation's to '.csv' files, to allow analysis.
'''
#######
#Set initial conditions
deltaT = 0.005               #Time-step
T = 0                        #Start time
endT =20                    #Duration
update_method =4             #1-Euler, 2-Euler-Cromer, 3-Euler-Richardson, 4 = Runge Kutta
df = 0.0                     #Damping Factor
NumberOfPendulums = 1       #1 - single pendulum, 2- Double pendulum (1 interation, energy/position analysis), 3- double pendulum (time analysis)

                    # position              velocity            acceleration    name   mass    theta          length  OMEGA       alpha        ORIGIN POINT E KE PE damping factor
pendulum1 = np.array([np.array([-4.,-3.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, 0., 1., [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], 0.0, 0.0, 0.0, df])
pendulum2 = np.array([np.array([-5.,-2.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, 0., 1., [0.,0.,0.], [0.,0.,0.], [-4.,-3.,0.], 0.0, 0.0, 0.0, df])

#Define list of x,y positions around origin-points for analysis
#Current set-up: length of 5, iterations every pi/6 radians.
a = (5. * (3.**0.5))/2.
initial_x_values =[-2.5 , -a , -5. , -a , -2.5 ,  0. , 2.5 , a, 5. ,a , 2.5, 0. ]                                              
initial_y_values =[a, 2.5 , 0. , -2.5 , -a ,  -5. , -a , -2.5 , 0. , 2.5 , a ,5]

#######



#######
#Run analysis of each system
#Then uses Pandas to save the returned simulation data to a '.csv' file.

if NumberOfPendulums == 1:
    listofobjects = [pendulum1]     #Allows single pendulum system to be investigated
    pendulums = DoublePendulum(listofobjects)   #Takes the inital data and makes them instances of the DoublePendulum class.
    time_analysis = 'N'
    data = pendulums.run_simulation(endT, deltaT, update_method, time_analysis)   #Calls the method which runs the simulation.
    data1 = pd.DataFrame(data = data[0], columns = ['mass','position','velocity','acceleration','angle','length','angular_velocity','angular_acceleration', 'time', 'tot_energy', 'kin_energy', 'pot_energy', 'damping_factor'])
    data1.to_pickle('Pendulum_testing_06_04.csv')   #Saves the simulation's data.
elif NumberOfPendulums == 2:
    listofobjects = [pendulum1, pendulum2]     #Allows double pendulum system to be investigated
    pendulums = DoublePendulum(listofobjects)   #Takes the inital data and makes them instances of the DoublePendulum class.
    time_analysis = 'N'
    data = pendulums.run_simulation(endT, deltaT, update_method, time_analysis)   #Calls the method which runs the simulation.
    data1 = pd.DataFrame(data = data[0], columns = ['mass','position','velocity','acceleration','angle','length','angular_velocity','angular_acceleration', 'time', 'tot_energy', 'kin_energy', 'pot_energy', 'damping_factor'])
    data2 = pd.DataFrame(data = data[1], columns = ['mass','position','velocity','acceleration','angle','length','angular_velocity','angular_acceleration', 'time', 'tot_energy', 'kin_energy', 'pot_energy', 'damping_factor'])
    data1.to_pickle('Pendulum_testing_06_04.csv')
    data2.to_pickle('Pendulum_testing2_06_04.csv')      #Saves the simulation's data.
elif NumberOfPendulums == 3:

    total_time_data = []                
    pos1 = [0.0, 0.0]
    pos2 = [0.0, 0.0]
    for i in range(0,len(initial_x_values)):
        for j in range(0,len(initial_y_values)):        #Loops through list of initial positions stated earlier.
            pos1 = np.array([initial_x_values[i],initial_y_values[i] ]) #Position of top pendulum
            pos2 = np.array([initial_x_values[i] +  initial_x_values[j] , initial_y_values[i] +  initial_y_values[j] ]) #Position of bottom pendulum
            
            #Creates two pendulum objects
            pendulum1 = np.array([np.array([initial_x_values[i],initial_y_values[i],0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, 0., 1., [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], 0.0, 0.0, 0.0, df])     
            pendulum2 = np.array([ np.array([initial_x_values[i] +  initial_x_values[j] , initial_y_values[i] +  initial_y_values[j] ,0.]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, 0., 1., [0.,0.,0.], [0.,0.,0.], [initial_x_values[i],initial_y_values[i],0.], 0.0, 0.0, 0.0, df])
            listofobjects = [pendulum1, pendulum2]      
            pendulums = DoublePendulum(listofobjects)
            time_analysis = 'Y'
            time_to_flip = pendulums.run_simulation(endT, deltaT, update_method, time_analysis)[0] #Runs time analysis for double pendulum
            if time_to_flip == 0.0:
                time_to_flip = 'no flip'
            
            total_time_data.append((pos1, pos2, time_to_flip))    #Stores time-to-flip data

    df = pd.DataFrame(data = total_time_data, columns = ['initial_pend1', 'initial_pend2', 'time_to_flip']) 
    df.to_pickle('Pendulum_time_analysis_06_04.csv')    #Uses Pandas to save all time analysis data to a '.csv' file.


#######
