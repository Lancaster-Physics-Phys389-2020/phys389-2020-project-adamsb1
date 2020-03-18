from Pendulum2 import Pendulum
import numpy as np
import math
import scipy.constants as sp
import copy
import pandas as pd 

class DoublePendulum(Pendulum):
    def __init__(self, listofobjects):
        self.pendulums = listofobjects

        for i in range(len(listofobjects)):
            self.pendulums[i] = Pendulum(self.pendulums[i][0],self.pendulums[i][1],self.pendulums[i][2],self.pendulums[i][3],self.pendulums[i][4],self.pendulums[i][5],self.pendulums[i][6],self.pendulums[i][7],self.pendulums[i][8],self.pendulums[i][9],self.pendulums[i][10],self.pendulums[i][11],self.pendulums[i][12],self.pendulums[i][13] )

    def __repr__(self):
        return 'Pendulum: %s' %(self.pendulums)

    def run_simulation(self,duration,deltaT,method):
        print('GAME ON')
        total_data1 = []
        total_data2 = []
        time = 0
        while time < duration:
            for i in range(0, len(self.pendulums)):
                self.pendulums[i].update(deltaT,method)
                pendulums_data = copy.deepcopy(self.pendulums)

            i = 0
            while i < 2:
                if i == 0:
                    total_data1.append([pendulums_data[i].mass, pendulums_data[i].position ,pendulums_data[i].velocity ,pendulums_data[i].acceleration, pendulums_data[i].angle, pendulums_data[i].length, pendulums_data[i].ang_velocity, pendulums_data[i].ang_acceleration, time,  pendulums_data[i].tot_energy, pendulums_data[i].kin_energy, pendulums_data[i].pot_energy, pendulums_data[i].damping_factor ])
                elif i == 1:
                    total_data2.append([pendulums_data[i].mass, pendulums_data[i].position ,pendulums_data[i].velocity ,pendulums_data[i].acceleration, pendulums_data[i].angle, pendulums_data[i].length, pendulums_data[i].ang_velocity, pendulums_data[i].ang_acceleration, time,  pendulums_data[i].tot_energy, pendulums_data[i].kin_energy, pendulums_data[i].pot_energy, pendulums_data[i].damping_factor ])
                i+=1
            time+=deltaT
        df = pd.DataFrame(data = total_data1, columns = ['mass','position','velocity','acceleration','angle','length','angular_velocity','angular_acceleration', 'time', 'tot_energy', 'kin_energy', 'pot_energy', 'damping_factor'])
        df.to_pickle('Pendulum_RK_1.csv')

        df = pd.DataFrame(data = total_data2, columns = ['mass','position','velocity','acceleration','angle','length','angular_velocity','angular_acceleration', 'time', 'tot_energy', 'kin_energy', 'pot_energy', 'damping_factor'])
        df.to_pickle('Pendulum_RK_2.csv')



