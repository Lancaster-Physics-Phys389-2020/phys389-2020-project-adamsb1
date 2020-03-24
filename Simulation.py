import math
import numpy as np 
from Particle import Particle
from Pendulum2 import Pendulum
from Double_Pendulum import DoublePendulum
import scipy.constants
import matplotlib.pyplot as plt
import pandas as pd 
import copy

deltaT = 0.005
T = 0
endT = 500

update_method =4                #1-euler, 2-cromer, 3-richardson, 4 = RK

df = 0.5

                    # position          velocity        acceleration name   mass    theta          length  OMEGA    alpha  ORIGIN POINT E KE PE, damping factor
pendulum1 = np.array([np.array([-4.,-3.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, scipy.constants.pi/2, 1., [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], 0.0, 0.0, 0.0, df])
#pendulum2 = np.array([np.array([4.,0.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 2, scipy.constants.pi/2, 1., [4.,3.,0.], [0.,0.,0.], [0.,0.,0.], 0.0, 0.0, 0.0, df])

listofobjects = [pendulum1    ] #, pendulum2]
#pend_ball_current = pendulum1
total_data1 = []
total_data2 = []

pendulums = DoublePendulum(listofobjects)
pendulums.run_simulation(endT, deltaT, update_method)

