from Pendulum2 import Pendulum
import numpy as np
import math
import scipy.constants as sp
import pandas as pd 
import copy

class DoublePendulum(Pendulum):
    '''
    This class runs the simulation by calling a number of subroutines, and returns the data necessary for analysis to take place.
    Given a list of data, it creates instance(s) of the pendulum object. 
    If there are two data sets, then two pendulum objects are created.

    Updating the system at each time-step is done by calling functions from the pendulum objects.

    Either returns position, and energy data or returns time-to-flip data.

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
        Using the time-step (deltaT) to update the system throught the duration of the system (duration), using the update method (method) specified.
        Returns simulation data ready for analysis.

        total_data(1/2)  -  Stores all the data collected from the system whilst it's running.
        time - running count of time (number of time-steps completed)
        '''
        
        total_data1 = []
        total_data2 = []
        time = 0
        n_pendulums = len(self.pendulums)       #Value is frequently used: states whether the system has one or two pendulums.
        while time < duration:
            flip = '' #Stops 'referenced before defined' error
            if n_pendulums > 1:
                self.pendulums[1].origin_point = self.pendulums[0].position     #If there are two pendulums, updates the orgin-point of the lower pendulum at each time-step
            pendulum_positions = self.call_update(n_pendulums, deltaT, method, flip)    #Calls the function used to update the system.
            for i in range(0,n_pendulums):
                    self.pendulums[i].position = pendulum_positions[i]      #Saves new data to each pendulum object.
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
            if time_analysis == 'Y':            #If time-to-flip analysis is taking place, and pendulum has flipped, breaks out of the loop to output the data..
                for i in range(0, n_pendulums):
                    if self.pendulums[i].flipped == 'yes': 
                        time_to_flip = time
                if time_to_flip > 0:
                    break

            time+=deltaT # Advances to the next time-step

        output_data = []
        if time_analysis == 'N':
            output_data.append( total_data1)
            if n_pendulums > 1:                         #Outputs the necessary data ( based on which type of analysis is taking place) from the simulation to allow analysis.
                output_data.append( total_data2)
        elif time_analysis == 'Y':
            output_data.append(time_to_flip)
        return output_data
        
    def second_pendulum_data(self, i):
        '''
        This function obtains all the data (not contained in the pendulum object) used to calculate acceleration in the double pendulum case.
        i.e. if the acceleration of the 'bottom' pendulum is being calculated, this function obtains data from the 'top' pendulum.
        '''
        if i == 1:
            P = 'B'
            j = 0
        elif i == 0:
            P = 'T'
            j = 1
        mass = self.pendulums[j].mass
        vel = self.pendulums[j].ang_velocity[2]
        l = self.pendulums[j].length
        ang = self.pendulums[j].angle
        return mass, vel, l, ang, P      #Returns mass, angular velocity, length, angle and position (top/bottom) of the other pendulum.

    def call_update(self, n_pendulums, deltaT, method, flip):
        '''
        This function calls the update fucntions (in Pendulum2.py), to update the pendulum's properties.
        Outputs the new positions.
        '''
        pendulums_new_positions = []
        P = ''
        mass = 0.0
        vel = np.array([0.0,0.0,0.0], dtype = float)    #Sets initial data types for variables used in update methods.
        l = 0.0
        ang = 0.0
        if n_pendulums > 1:         #Double pendulum system
            for i in range(0, n_pendulums):
                mass, vel, l, ang, P = self.second_pendulum_data(i)    #Determines the values of the extra data required for the 'other' pendulum.
                pendulums_new_positions.append(self.pendulums[i].update(deltaT,method, n_pendulums, P, mass, vel, l, ang, flip) ) #Updates the Pendulum object's data, saving the new position.
        else:   
            pendulums_new_positions.append( self.pendulums[0].update(deltaT,method, n_pendulums, P, mass, vel, l, ang, flip) )
        return pendulums_new_positions
           
