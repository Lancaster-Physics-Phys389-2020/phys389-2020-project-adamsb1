import numpy as np
import math
import copy
import scipy.constants

class Particle:
    """
    Class to model a masses at the end of the pendulums. 
    It will be used as an inheritance class for Pendulum. 

    mass in kg 
    position and velocity in m 
    """

    #G=6.67408E-11
    G=scipy.constants.G

    def __init__(self, Position=np.array([0,0], dtype=float), Velocity=np.array([0,0], dtype=float), Acceleration=np.array([0,-10], dtype=float), Name='Ball', Mass=1.0):
        '''
        Creates a new instance of 'Particle', giving the object this class' properties.
        '''
        self.Name = Name
        self.position = np.array(Position,dtype=float)
        self.velocity = np.array(Velocity,dtype=float)              #Initital properties of object.
        self.acceleration = np.array(Acceleration,dtype=float)
        self.mass = Mass

    def __repr__(self):
        return 'Particle: {0}, Mass: {1:12.3e}, Position: {2}, Velocity: {3}, Acceleration: {4}'.format(self.Name,self.mass,self.position, self.velocity,self.acceleration)


 