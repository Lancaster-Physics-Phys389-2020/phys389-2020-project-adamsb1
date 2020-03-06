from Particle import Particle
import numpy as np
import math
import scipy.constants as sp

class Pendulum(Particle):



    def __init__(self, position=np.array([0,0,0], dtype=float), velocity=np.array([0,0,0], dtype=float), acceleration=np.array([0.,0.,0.], dtype=float), name='Ball', mass=1.0, angle = 0.0, length = 0.0, ang_velocity =np.array([ 0.,0.,0.], dtype=float), ang_acceleration = np.array([0.,0.,0.], dtype=float), origin_point = np.array([0.,0.,0.], dtype = float) , tot_energy = 0.0, kin_energy = 0.0, pot_energy = 0.0, damping_factor= 0.0  ):
        super().__init__(position , velocity, acceleration,name, mass)
        self.origin_point = origin_point
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



    def update(self, deltaT, update_method):
        

        if update_method == 1:
            self.update_euler(deltaT)
        elif update_method == 2:
            self.update_cromer(deltaT)
        elif update_method == 3:
            self.update_richardson(deltaT)
        elif update_method == 4:
            self.update_runge_kutter(deltaT)
        
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

    def update_euler(self, deltaT):
        '''
        Updates the velocity and position of the object by time-step (deltaT), using the Euler algorithm.
        Position first then velocity.
        '''
        self.ang_acceleration[2] = self.damped_sho(self.angle, self.ang_velocity)

        self.angle += self.ang_velocity[2] * deltaT
        self.ang_velocity[2] += self.ang_acceleration[2] * deltaT
        

    def update_cromer(self, deltaT):
        '''
        Updates the velocity and position of the object by time-step (deltaT), using the Euler-Cromer algorithm.
        Velocity first then position
        '''
        self.ang_acceleration[2] = self.damped_sho(self.angle, self.ang_velocity)

        self.ang_velocity[2] += self.ang_acceleration[2] * deltaT
        self.angle += self.ang_velocity[2] * deltaT


    def update_richardson(self, deltaT):
        angle_mid = self.angle + self.ang_velocity[2] * (deltaT/2.0)
        ang_velocity_mid =self.ang_velocity[2] + self.ang_acceleration[2] * (deltaT/2.0)
        
        ang_acceleration_mid = self.damped_sho(angle_mid, ang_velocity_mid)

        self.ang_acceleration[2] = self.damped_sho(self.angle, self.ang_velocity)
        self.angle += ang_velocity_mid * deltaT
        self.ang_velocity[2] += ang_acceleration_mid * deltaT

    def update_runge_kutter(self, deltaT):
        #i hate this method
        k_ang = [0.0]*4
        k_vel = [0.0]*4
        k_acc = [0.0]*4
        print('k_ang' , k_ang)
        i=0
        while i < 4:
            print(i)
             
            angle = self.angle
            velocity = self.ang_velocity
            acceleration = self.ang_acceleration
            if i == 0:
               

                #RK: k_1 = deltaT * f(x,y,z)
                #RK: k_2 = deltaT * f(x + k_1_x/2, y + k_1_y/2, y + k_1_z/2)
                #RK: k_3 = deltaT * f(x + k_2_x/2, y + k_2_y/2, y + k_2_z/2)
                #RK: k_4 = deltaT * f(x + k_3_x, y + k_3_y, y + k_3_z)



                k_ang[i], k_vel[i], k_acc[i] = (self.calc_k(angle, velocity, np.array(acceleration), deltaT))               #acceleration=np.array([0.,0.,0.], dtype=float)
            elif i ==1 or i == 2:

                k_ang[i], k_vel[i], k_acc[i] = self.calc_k( angle = (angle + k_ang[i-1]/2) , velocity = np.array([0.0,0.0,velocity[2] + (k_vel[i-1]/2)]), acceleration = np.array([0.0,0.0,acceleration[2] + (k_acc[i-1]/2)]), deltaT = (deltaT/2)) 
            else:
                k_ang[i], k_vel[i], k_acc[i] = self.calc_k( (angle + k_ang[i-1]) , velocity = np.array([0.0,0.0,velocity[2] + (k_vel[i-1])]), acceleration =  np.array([0.0,0.0,acceleration[2] + (k_acc[i-1])]), deltaT =deltaT ) 

            i+=1
        print('inital angle', self.angle)
       
        self.ang_acceleration[2] = self.damped_sho(self.angle, self.ang_velocity) + ((k_acc[0] + (2*k_acc[1]) + (2*k_acc[2]) + k_acc[3]) *deltaT) / 6

        delta_vel = k_vel[0] *deltaT + (2.*k_vel[1])*deltaT + (2.*k_vel[2])*deltaT + k_vel[3]*deltaT
        delta_vel =delta_vel/ 6.

        self.angle += (delta_vel) 
        #((k_vel[0] + (2*k_vel[1]) + (2*k_vel[2]) + k_vel[3]) *deltaT) / 6

        delta_acc = k_acc[0] *deltaT + (2*k_acc[1])*deltaT + (2*k_acc[2])*deltaT + k_acc[3]*deltaT
        delta_acc =delta_acc/ 6.


        self.ang_velocity[2] += (delta_acc )
        #((k_acc[0] + (2*k_acc[1]) + (2*k_acc[2]) + k_acc[3]) *deltaT) / 6



        print('angle' , self.angle)
        print('k_ang' , k_ang)


    def calc_k(self, angle, velocity, acceleration, deltaT):
        acceleration[2] = self.damped_sho(angle, velocity)         #change in acc
        angle = velocity[2] * deltaT   
                                 #change in angle
        velocity = acceleration[2] * deltaT                        #change in vel

        return angle, velocity, acceleration