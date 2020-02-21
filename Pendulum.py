from Particle import Particle
import numpy as np
import math

class Pendulum(Particle):
    """
    """

    def __init__(self, Position=np.array([0,0,0], dtype=float), Velocity=np.array([0,0,0], dtype=float), Acceleration=np.array([0,-10,0], dtype=float), Name='Ball', Mass=1.0, Theta=1.0, Length = 1., omega=1.0, alpha=1.0 ):
        super().__init__(Position=Position, Velocity=Velocity, Acceleration=Acceleration, Name=Name, Mass=Mass)
        self.theta = np.arctan(self.position[0]/self.position[1])
        self.length = np.linalg.norm(self.position)
        self.omega = np.linalg.norm(np.cross(self.position, self.velocity)/(self.length**2))
        self.alpha = alpha


    def __repr__(self):
        return 'Particle: {0}, Mass: {1:12.3e}, Position: {2}, Velocity: {3}, Acceleration: {4}, Theta: {5}, Length: {6}, Omega: {7}, Alpha: {8}'.format(self.Name,self.mass,self.position, self.velocity,self.acceleration,self.theta,self.length, self.omega, self.alpha)

    g=9.81


    def update(self, deltaT):
        self.alpha = -(9.81/self.length) * math.sin(self.theta)
        
        self.omega += self.alpha * deltaT
        
        self.theta += self.omega * deltaT
        
        
