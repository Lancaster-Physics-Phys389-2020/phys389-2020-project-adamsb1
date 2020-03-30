import math
import numpy as np 
from Particle import Particle
from Pendulum2 import Pendulum
from Double_Pendulum import DoublePendulum
import scipy.constants



#This file is used to set the initial condidtions of the system, including all data for the pendulums, time-step size, duration of the simulation, update method and damping factor.

#######
#Set initial conditions
deltaT = 0.005  #Time-step
T = 0
endT = 500       #Duration
update_method =3              #1-Euler, 2-Euler-Cromer, 3-Euler-Richardson, 4 = Runge Kutta
df = 0.01       #Damping Factor

                    # position              velocity            acceleration    name   mass    theta          length  OMEGA       alpha        ORIGIN POINT E KE PE damping factor
pendulum1 = np.array([np.array([-4.,-3.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, 0., 1., [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], 0.0, 0.0, 0.0, df])
#pendulum2 = np.array([np.array([-4.,3.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, 0., 1., [0.,0.,0.], [0.,0.,0.], [-4.,0.,0.], 0.0, 0.0, 0.0, df])
#######



#######
#Run program 

listofobjects = [pendulum1] #, pendulum2]      #Allows double pendulum system to be ran, to chage for single pendulum, remove ", pendulum2"
pendulums = DoublePendulum(listofobjects)   #Takes the inital data and makes them instances of the DoublePendulum class.
pendulums.run_simulation(endT, deltaT, update_method)   #Calls the method which runs the simulation.

#######