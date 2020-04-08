from Pendulum2 import Pendulum
import numpy as np
import math
import scipy.constants as sp
import pandas as pd 
import copy

class DoublePendulum(Pendulum):
    '''
    This class runs the simulation by calling a number of subroutines, save the data, and outputs it to a storage file.
    Given a list of data, it creates an instance of the pendulum object. 
    If there are two data sets, then two pendulum objects are created.

    Updating the system at each time-step is done by calling fucntions from the pendulum objects.

    Either saves energy data as a .csv file via pandas or returns time-to-flip data.

    '''
    def __init__(self, listofobjects):
        ''' 
        Constructor class
        self - instance of the program
        listofobjects - data inputted into the system to create the pendulum object(s).
        '''
        self.pendulums = listofobjects

        for i in range(len(listofobjects)): #Allows two pendulum objects (with discrete properties) to be created and stored in a list
            self.pendulums[i] = Pendulum(self.pendulums[i][0],self.pendulums[i][1],self.pendulums[i][2],self.pendulums[i][3],self.pendulums[i][4],self.pendulums[i][5],self.pendulums[i][6],self.pendulums[i][7],self.pendulums[i][8],self.pendulums[i][9],self.pendulums[i][10],self.pendulums[i][11],self.pendulums[i][12],self.pendulums[i][13] )

    def __repr__(self):
        return 'Pendulum: %s' %(self.pendulums)

    def run_simulation(self,duration,deltaT,method, time_analysis):
        '''
        This method controls the simulation.
        Using the time-step (deltaT) to update the system throught he duration of the system (duration), using the update method (method) specified.
        Either saves energy data via pandas or returns time-to-flip data.

        total_data(1/2)  -  Stores all the data collected from the system whilst its running.
        time - running count of time (number of time-steps completed)
        '''
        
        total_data1 = []
        total_data2 = []
        time = 0
        n_pendulums = len(self.pendulums)       #Value is frequently used: states whether the system has one or two pendulums.
        #print(len(self.pendulums))
        while time < duration:
            print(time)
            flip = ''
            P = ''
            mass = 0.0
            vel = np.array([0.0,0.0,0.0], dtype = float)    #Sets initial data types for variables used in update methods.
            l = 0.0
            ang = 0.0
            if n_pendulums > 1:         #Double pendulum system
                for i in range(0, n_pendulums):
                   
                    if i == 0:          #Determines the values of the extra data required for the 'top pendulum'
                        self.pendulums[1].origin_point = self.pendulums[0].position
                        P = 'T'
                        mass = self.pendulums[1].mass
                        vel = self.pendulums[1].ang_velocity[2]
                        l = self.pendulums[1].length
                        ang = self.pendulums[1].angle
                
                    elif i == 1:        #Determines the values of the extra data required for the 'bottom pendulum'
                        P = 'B'
                        mass = self.pendulums[0].mass
                        vel = self.pendulums[0].ang_velocity[2]
                        l = self.pendulums[0].length
                        ang = self.pendulums[0].angle
                    self.pendulums[i].update(deltaT,method, n_pendulums, P, mass, vel, l, ang, flip)  #Updates the Pendulum object's data
            else:   #Single Pendulum system
                self.pendulums[0].update(deltaT,method, n_pendulums, P, mass, vel, l, ang, flip)
            pendulums_data = copy.deepcopy(self.pendulums)  #Creates a copy of all the system data without deleting the original data in 'self.pendulums'
           

            if (time//(deltaT*1000))%1 == 0 or time == 0:   #Reduces amount of data collected (by factor of 10) without reducing accuracy of data.
                #Saves the system data into two lists: total_data1 and total_data2
                i = 0
                while i < 2:
                    if i == 0:
                        total_data1.append(copy.deepcopy([pendulums_data[i].mass, pendulums_data[i].position ,pendulums_data[i].velocity ,pendulums_data[i].acceleration, pendulums_data[i].angle, pendulums_data[i].length, pendulums_data[i].ang_velocity, pendulums_data[i].ang_acceleration, time,  pendulums_data[i].tot_energy, pendulums_data[i].kin_energy, pendulums_data[i].pot_energy, pendulums_data[i].damping_factor ]))
                    elif i == 1:
                        if n_pendulums>1:
                            total_data2.append([pendulums_data[i].mass, pendulums_data[i].position ,pendulums_data[i].velocity ,pendulums_data[i].acceleration, pendulums_data[i].angle, pendulums_data[i].length, pendulums_data[i].ang_velocity, pendulums_data[i].ang_acceleration, time,  pendulums_data[i].tot_energy, pendulums_data[i].kin_energy, pendulums_data[i].pot_energy, pendulums_data[i].damping_factor ])
                    i+=1

            time_to_flip = 0.0
            if time_analysis == 'Y':            #If time-to-flip analysis is taking place, and pendulum has flipped. Returns the time it took before the pednulum flipped (breaks out of the loop).
                for i in range(0, n_pendulums):
                    if self.pendulums[i].flipped == 'yes': 
                        time_to_flip = time
                        if time_to_flip > 0:
                            return time_to_flip
                        else:
                            return 'no flip'



            time+=deltaT # Advances to the next time-step
        
        #Saves the data to an external .csv file using Pandas, when energy is being investigated

        #Returns the time it took for the pendulum to flip (When time-to-flip being analysed).

        if time_analysis == 'N':
            df = pd.DataFrame(data = total_data1, columns = ['mass','position','velocity','acceleration','angle','length','angular_velocity','angular_acceleration', 'time', 'tot_energy', 'kin_energy', 'pot_energy', 'damping_factor'])
            df.to_pickle('Pendulum_testing_06_04.csv')
            if n_pendulums > 1:
                df = pd.DataFrame(data = total_data2, columns = ['mass','position','velocity','acceleration','angle','length','angular_velocity','angular_acceleration', 'time', 'tot_energy', 'kin_energy', 'pot_energy', 'damping_factor'])
                df.to_pickle('Pendulum_testing2_06_04.csv')
        
        





