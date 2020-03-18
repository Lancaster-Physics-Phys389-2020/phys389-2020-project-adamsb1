from Particle import Particle
import numpy as np
import math
import scipy.constants as sp

class Pendulum(Particle):
    def __init__(self, position=np.array([0,0,0], dtype=float), velocity=np.array([0,0,0], dtype=float), acceleration=np.array([0.,0.,0.], dtype=float), name='Ball', mass=1.0, angle = 0.0, length = 0.0, ang_velocity =np.array([ 0.,0.,0.], dtype=float), ang_acceleration = np.array([0.,0.,0.], dtype=float), origin_point = np.array([0.,0.,0.], dtype = float) , tot_energy = 0.0, kin_energy = 0.0, pot_energy = 0.0, damping_factor= 0.0  ):
        super().__init__(position , velocity, acceleration,name, mass)
        self.origin_point = origin_point
        print('origin point: ', self.origin_point)
        self.length , self.angle = self.cart_to_pol_position()
        self.ang_velocity =[0.0, 0.0, (np.linalg.norm(self.velocity)) / self.length] 
        self.ang_acceleration = [0.0,0.0, 0.0] 
        self.damping_factor = damping_factor
        self.tot_energy , self.kin_energy, self.pot_energy = self.calculate_E()
    
    def __repr__(self):
        return '{0:12.3e},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}'.format(self.mass,self.position, self.velocity,self.acceleration,self.angle,self.length, self.ang_velocity, self.ang_acceleration, self.tot_energy, self.kin_energy, self.pot_energy)

    def cart_to_pol_position(self):
        x,y = self.delta_values() #
        rho = np.sqrt(x**2. + y**2.)
        phi = np.arctan2(y,x) + (sp.pi/2)  #sets origin directly below origin
        if phi> sp.pi:
            phi = phi -sp.pi * 2.           #All angles point to origin point, via shortest route
        return rho, phi

    def delta_values(self):
        delta_x = self.position[0] - self.origin_point[0]
        delta_y = self.position[1] - self.origin_point[1]
        return delta_x, delta_y

    def update(self, deltaT, update_method, n_pendulums, P, mass, vel, l, ang):

        if update_method == 1:
            self.update_euler(deltaT, n_pendulums, P, mass, vel, l, ang)
        elif update_method == 2:
            self.update_cromer(deltaT, n_pendulums, P, mass, vel, l, ang)
        elif update_method == 3:
            self.update_richardson(deltaT, n_pendulums, P, mass, vel, l, ang)
        elif update_method == 4:
            self.update_RK(deltaT, n_pendulums, P, mass, vel, l, ang)
        
        self.tot_energy, self.kin_energy, self.pot_energy = self.calculate_E()
        
        if self.angle> sp.pi:
            self.angle -= 2* sp.pi
        elif self.angle < -sp.pi:
            self.angle += 2* sp.pi

        x,y = self.pol_to_cart()
        self.position = np.array([x,y,0.], dtype = float)

    def calculate_E(self):
        KE = (0.5) * (self.mass) * ((self.length)**2.) * ((np.linalg.norm(self.ang_velocity)**2.))
        PE = (self.mass) * 9.81 * self.length * (1 - np.cos(self.angle))      #defines 0 PE at lowest point of swing
        E = KE + PE
        return E, KE, PE

    def pol_to_cart(self):
        delta_x = self.length * np.cos(self.angle - sp.pi/2)
        delta_y = self.length * np.sin(self.angle - sp.pi/2)
        x = delta_x - self.origin_point[0]
        y = delta_y - self.origin_point[1]
        return x , y

    def damped_sho(self, angle, ang_velocity):   
        if self.ang_velocity[2] >=0:
            f = 1
        else:
            f = -1
        ang_acceleration = ( (- 9.81 / (self.length)) * np.sin(angle)  ) - f * self.damping_factor * np.linalg.norm(ang_velocity) 
        return ang_acceleration

    def update_euler(self, deltaT, n_pendulums, P, mass, vel, l, ang):
        '''
        Updates the velocity and position of the object by time-step (deltaT), using the Euler algorithm.
        Position first then velocity.
        '''
        self.ang_acceleration[2] = self.determine_acc_method(self.angle, self.ang_velocity, n_pendulums, P, mass, vel, l, ang)
        #self.damped_sho(self.angle, self.ang_velocity)

        self.angle += self.ang_velocity[2] * deltaT
        self.ang_velocity[2] += self.ang_acceleration[2] * deltaT
        
    def update_cromer(self, deltaT, n_pendulums, P, mass, vel, l, ang):
        '''
        Updates the velocity and position of the object by time-step (deltaT), using the Euler-Cromer algorithm.
        Velocity first then position
        '''
        self.ang_acceleration[2] = self.determine_acc_method(self.angle, self.ang_velocity, n_pendulums, P, mass, vel, l, ang)
        #self.damped_sho(self.angle, self.ang_velocity)

        self.ang_velocity[2] += self.ang_acceleration[2] * deltaT
        self.angle += self.ang_velocity[2] * deltaT

    def update_richardson(self, deltaT, n_pendulums, P, mass, vel, l, ang):
        angle_mid = self.angle + self.ang_velocity[2] * (deltaT/2.0)
        ang_velocity_mid =self.ang_velocity[2] + self.ang_acceleration[2] * (deltaT/2.0)
        
        ang_acceleration_mid = self.determine_acc_method(angle_mid, ang_velocity_mid, n_pendulums, P, mass, vel, l, ang)
        #self.damped_sho(angle_mid, ang_velocity_mid)

        self.ang_acceleration[2] = self.determine_acc_method(self.angle, self.ang_velocity, n_pendulums, P, mass, vel, l, ang)
        #self.damped_sho(self.angle, self.ang_velocity)
        self.angle += ang_velocity_mid * deltaT
        self.ang_velocity[2] += ang_acceleration_mid * deltaT

    def update_RK(self, deltaT, n_pendulums, P, mass, vel, l, ang):
        self.ang_acceleration[2] = self.determine_acc_method(self.angle, self.ang_velocity, n_pendulums, P, mass, vel, l, ang)
        #self.damped_sho(self.angle, self.ang_velocity)

        k_a = [0.,0.,0.,0.]        #pos
        k_b = [0.,0.,0.,0.]        #vel

        k_a[0] = self.ang_velocity[2] * deltaT
        k_b[0] = (self.ang_acceleration[2] ) *deltaT


        k_a[1] = (self.ang_velocity[2] + (k_b[0]/2.)) * deltaT
        ang = self.angle + (k_a[0]*0.5)
        ang_vel = np.array([0.0, 0.0, 0.0 ] , dtype = float)
        acc = self.determine_acc_method(ang, ang_vel, n_pendulums, P, mass, vel, l, ang)
        #self.damped_sho(ang, vel)
        k_b[1] = acc *deltaT

        k_a[2] = (self.ang_velocity[2] + (k_b[1]/2.)) * deltaT
        ang = self.angle + (k_a[1]*0.5)
        ang_vel = np.array([0.0, 0.0, 0.0] , dtype = float)
        acc = self.determine_acc_method(ang, ang_vel, n_pendulums, P, mass, vel, l, ang)
        #self.damped_sho(ang, vel)
        k_b[2] = acc *deltaT

        k_a[3] = (self.ang_velocity[2] + k_b[2]) * deltaT
        ang = self.angle + (k_a[2])
        ang_vel = np.array([0.0, 0.0, 0.0] , dtype = float)
        acc = self.determine_acc_method(ang, ang_vel, n_pendulums, P, mass, vel, l, ang)
        #self.damped_sho(ang, vel)
        k_b[3] = acc *deltaT


        x = ((k_b[0] + 2*k_b[1] + 2*k_b[2] + k_b[3])/6.)
        self.ang_velocity[2] += x
        self.angle +=  ((k_a[0] + 2*k_a[1] + 2*k_a[2] + k_a[3])/6.)
        self.ang_acceleration[2] = self.determine_acc_method(self.angle, self.ang_velocity, n_pendulums, P, mass, vel, l, ang)
        #self.damped_sho(self.angle, self.ang_velocity)


    def determine_acc_method(self, angle, ang_velocity, n_pendulums, P, mass, vel, l, ang):
        if n_pendulums == 2:    
            print('doing right update')    
            ang_acc = self.double_pendulum_acc(angle, ang_velocity, P, mass, vel, l, ang)
        else:
            print()
            print('dam it')
            print()
            ang_acc = self.damped_sho(angle, ang_velocity)
        return ang_acc

    def double_pendulum_acc(self,angx,ang_vel, P, mass, vel, l, ang):
        g = 9.81

        if P == 'T':
            a = -g*(2.*self.mass + mass)*np.sin(self.angle)
            b = -mass*g*np.sin(angx - 2.*ang)
            c = -2.*mass*np.sin(angx - ang)
            d = (vel**2. * l) + (  (ang_vel[2])**2. *self.length * np.cos(angx - ang)  )
            num = a + b +(c*d)
            den = self.length *( 2.*self.mass + mass -  mass*np.cos(2.*angx - 2.*ang) )
            acc = num/den
        elif P == 'B':
            a = 2.*np.sin(ang - angx)
            b = vel**2. * l * (mass +self.mass)
            c = g * (mass + self.mass) * np.cos(ang)
            d = (ang_vel[2]**2.) * self.length * self.mass *np.cos(ang - angx)
            num = a*(b+c+d)
            den = self.length * (2. * mass + self.mass - self.mass * np.cos( 2.*ang - 2.*angx))
            acc = num/den

        return acc











