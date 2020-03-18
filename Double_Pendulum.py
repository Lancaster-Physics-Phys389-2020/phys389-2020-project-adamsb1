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
        n_pendulums = len(self.pendulums)
        while time < duration:
            P = ''
            mass = 0.0
            vel = np.array([0.0,0.0,0.0], dtype = float) 
            l = 0.0
            ang = 0.0
            if n_pendulums > 1:
                for i in range(0, n_pendulums):
                   
                    if i == 0:
                        self.pendulums[1].origin_point = self.pendulums[0].position
                        print('origin: ',self.pendulums[1].origin_point)
                        print('position: ',self.pendulums[1].position)

                        P = 'T'
                        mass = self.pendulums[1].mass
                        vel = self.pendulums[1].ang_velocity[2]
                        l = self.pendulums[1].length
                        ang = self.pendulums[1].angle
                
                    elif i == 1:
                        P = 'B'
                        mass = self.pendulums[0].mass
                        vel = self.pendulums[0].ang_velocity[2]
                        l = self.pendulums[0].length
                        ang = self.pendulums[0].angle

                self.pendulums[i].update(deltaT,method, n_pendulums, P, mass, vel, l, ang)
            else:
                self.pendulums[0].update(deltaT,method, n_pendulums, P, mass, vel, l, ang)
            pendulums_data = copy.deepcopy(self.pendulums)
            print(time)
            i = 0
            while i < 2:
                if i == 0:
                    total_data1.append([pendulums_data[i].mass, pendulums_data[i].position ,pendulums_data[i].velocity ,pendulums_data[i].acceleration, pendulums_data[i].angle, pendulums_data[i].length, pendulums_data[i].ang_velocity, pendulums_data[i].ang_acceleration, time,  pendulums_data[i].tot_energy, pendulums_data[i].kin_energy, pendulums_data[i].pot_energy, pendulums_data[i].damping_factor ])
                elif i == 1:
                    if n_pendulums>1:
                     total_data2.append([pendulums_data[i].mass, pendulums_data[i].position ,pendulums_data[i].velocity ,pendulums_data[i].acceleration, pendulums_data[i].angle, pendulums_data[i].length, pendulums_data[i].ang_velocity, pendulums_data[i].ang_acceleration, time,  pendulums_data[i].tot_energy, pendulums_data[i].kin_energy, pendulums_data[i].pot_energy, pendulums_data[i].damping_factor ])
                i+=1

            time+=deltaT




        df = pd.DataFrame(data = total_data1, columns = ['mass','position','velocity','acceleration','angle','length','angular_velocity','angular_acceleration', 'time', 'tot_energy', 'kin_energy', 'pot_energy', 'damping_factor'])
        df.to_pickle('Pendulum_RK_1.csv')

        df = pd.DataFrame(data = total_data2, columns = ['mass','position','velocity','acceleration','angle','length','angular_velocity','angular_acceleration', 'time', 'tot_energy', 'kin_energy', 'pot_energy', 'damping_factor'])
        df.to_pickle('Pendulum_RK_2.csv')



