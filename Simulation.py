import math
import numpy as np 
from Particle import Particle
from Pendulum import Pendulum
import scipy.constants
import matplotlib
import pandas as pd 

deltaT = 0.01
T = 0
endT = 20

pend_ball = Pendulum(np.array([1,0,0]),np.array([0,0,0]),np.array([0,0,0]),'ball', 1, scipy.constants.pi/2, 1., 0., 0. )

print("theta after inheritance",pend_ball.theta)
while T <= endT:
    T += deltaT
    pend_ball.update(deltaT)
    print(pend_ball)