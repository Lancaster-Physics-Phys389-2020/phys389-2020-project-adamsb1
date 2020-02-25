from Particle import Particle
import numpy as np
import math
import scipy.constants as sp

class Pendulum(Particle):
    """
    """

    def __init__(self, Position=np.array([0,0], dtype=float), Velocity=np.array([0,0], dtype=float), Acceleration=np.array([0,-10], dtype=float), Name='Ball', Mass=1.0, Theta=1.0, Length = 1., omega=1.0, alpha=1.0 ):
        super().__init__(Position=Position, Velocity=Velocity, Acceleration=Acceleration, Name=Name, Mass=Mass)
        self.theta = np.arctan(self.position[0]/self.position[1])
        self.length = np.linalg.norm(self.position)
        self.omega = np.linalg.norm(np.cross(self.position, self.velocity)/(self.length**2))
        self.alpha = alpha


    def __repr__(self):
        return '{0:12.3e},{1},{2},{3},{4},{5},{6},{7}'.format(self.mass,self.position, self.velocity,self.acceleration,self.theta,self.length, self.omega, self.alpha)

    g=9.81


    def update(self, deltaT):
        self.alpha = -(9.81/self.length) * math.sin(self.theta)
        self.omega += self.alpha * deltaT
        self.theta += self.omega * deltaT
        if self.theta> sp.pi:
            self.theta -= 2* sp.pi

        
        
