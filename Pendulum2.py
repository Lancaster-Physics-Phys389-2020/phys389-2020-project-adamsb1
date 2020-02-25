from Particle import Particle
import numpy as np
import math
import scipy.constants as sp

class Pendulum(Particle):



    def __init__(self, position=np.array([0,0,0], dtype=float), velocity=np.array([0,0,0], dtype=float), acceleration=np.array([0.,0.,0.], dtype=float), name='Ball', mass=1.0, angle = 0.0, length = 0.0, ang_velocity =np.array([ 0.,0.,0.], dtype=float), ang_acceleration = np.array([0.,0.,0.], dtype=float), origin_point = np.array([0.,0.,0.], dtype = float)  ):
        super().__init__(position , velocity, acceleration,name, mass)
        self.origin_point = origin_point
        self.length , self.angle = self.cart_to_pol_position()
        self.ang_velocity =[0.0, 0.0, (np.sqrt(self.velocity[0] **2. + self.velocity[1]**2.)) / self.length] 
        self.ang_acceleration = [0.0,0.0,  (np.sqrt(self.acceleration[0] **2. + self.acceleration[1]**2.)) / self.length] 
        


    def __repr__(self):
        return '{0:12.3e},{1},{2},{3},{4},{5},{6},{7}'.format(self.mass,self.position, self.velocity,self.acceleration,self.angle,self.length, self.ang_velocity, self.ang_acceleration)

    def cart_to_pol_position(self):
        x,y = self.delta_values()
        rho = np.sqrt(x**2. + y**2.)
        phi = np.arctan2(y,x) + (sp.pi/2)  #sets origin directly below origin
        if phi> sp.pi:
            phi = phi -sp.pi * 2.           #All angles point to origin point, via shortest route
        return rho, phi


    def delta_values(self):
        delta_x = self.position[0] - self.origin_point[0]
        delta_y = self.position[1] - self.origin_point[1]
        return delta_x, delta_y



    def update(self, deltaT):
        self.ang_acceleration = -(9.81/self.length) * math.sin(self.angle)
        self.ang_velocity += self.ang_acceleration * deltaT
        self.angle += self.ang_velocity[2] * deltaT
        if self.angle> sp.pi:
            self.angle -= 2* sp.pi
        elif self.angle < -sp.pi:
            self.angle += 2* sp.pi

        #x,y = self.pol_to_cart()
        #self.position = 




    def pol_to_cart(self):
        delta_x = self.length * np.cos(self.angle)
        delta_y = self.length * np.sin(self.angle)

        return delta_x , delta_y
