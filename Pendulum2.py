from Particle import Particle
import numpy as np
import math
import scipy.constants as sp

class Pendulum(Particle):
    '''
    This class is used to model the pendulum's behaviour.
    It inherits the Particle class.
    Several update methods are found in this class.
    Calculates all data required to analyse system (including: position (cartesian and polar), kinetic energy, potential energy and total energy).
    Also contains acceleration methods necessary for boht single and double pendulum systems.
    '''
    def __init__(self, position=np.array([0,0,0], dtype=float), velocity=np.array([0,0,0], dtype=float), acceleration=np.array([0.,0.,0.], dtype=float), name='Ball', mass=1.0, angle = 0.0, length = 0.0, ang_velocity =np.array([ 0.,0.,0.], dtype=float), ang_acceleration = np.array([0.,0.,0.], dtype=float), origin_point = np.array([0.,0.,0.], dtype = float) , tot_energy = 0.0, kin_energy = 0.0, pot_energy = 0.0, damping_factor= 0.0, flipped = 'no' ):
        '''
        Constructor class for the program
        Creates a new 'Pendulum' instance, such that an object can inherit this class' properties.

        self - instance of the object
        Other values are inital values of the object.
        '''
        super().__init__(position , velocity, acceleration,name, mass)      #Inherits the properrties from the 'Particle' class.
        self.origin_point = origin_point
        if position[0] == 0. and position[1] == 0.0:
            self.length = length
            self.angle = angle
        else:
            self.length , self.angle = self.cart_to_pol_position()
        if velocity[0] != 0 and velocity[1] != 0:
            self.ang_velocity =[0.0, 0.0, (np.linalg.norm(self.velocity)) / self.length]                #Calculates all the initial properties of the new 'Pendulum' object, given the initial values. 
        else:
            self.ang_velocity = ang_velocity
        self.ang_acceleration = [0.0,0.0, 0.0] 
        self.damping_factor = damping_factor
        self.tot_energy , self.kin_energy, self.pot_energy = self.calculate_E()
        self.flipped = flipped
    
    def __repr__(self):
        return '{0:12.3e},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12}'.format(self.mass,self.position, self.velocity,self.acceleration,self.angle,self.length, self.ang_velocity, self.ang_acceleration, self.tot_energy, self.kin_energy, self.pot_energy, self.damping_factor, self.flipped)

    def cart_to_pol_position(self):
        '''
        Converts position in cartesian coordinates to position in polar coordinates.
        x,y - cartesian coordinates
        phi,rho - polar coordinates
        '''
        x,y = self.delta_values()           #Allows length of pendulum to be calculated regardless of origin point.
        rho = np.sqrt(x**2. + y**2.)
        phi = np.arctan2(y,x) + (sp.pi/2)  #Sets 0 point of angle directly below origin.
        if phi> sp.pi:
            phi = phi -sp.pi * 2.           #All angles point to 0 point, via shortest route ( -pi < angle < pi)
        return rho, phi

    def pol_to_cart(self):
        '''
        Converts position in polar coordinates to position in cartesian coordinates.
        x,y - cartesian coordinates
        phi,rho - polar coordinates
        '''
        delta_x = self.length * np.cos(self.angle - sp.pi/2)        #Convert to polar
        delta_y = self.length * np.sin(self.angle - sp.pi/2)
        x = delta_x + self.origin_point[0]                  
        y = delta_y + self.origin_point[1]          #Takes into account origin point of pendulum with respect to rest of system.
        if y < (10. * 10. ** -10) and y > -(10. * 10. ** -10):
            y = 0
        if x < (10. * 10. ** -10) and x > -(10. * 10. ** -10):
            x = 0
        return x , y

    def delta_values(self):
        '''
        Determines the difference in current position and origin point
        '''
        delta_x = self.position[0] - self.origin_point[0]
        delta_y = self.position[1] - self.origin_point[1]
        return delta_x, delta_y

    def update(self, deltaT, update_method, n_pendulums, P, mass, vel, l, ang, flip):
        '''
        This function controls how the system changes per time-step (deltaT)

        update_method - holds an integer which referes to which update method is being used
        n_pendulums - an integer which refers to the number of pendulums the system is simulating (either 1 or 2)
        P - holds a string (either 'T' or 'B'), used to determine which pendulum is being updated (for use in double pendulum)
        mass, vel, l, ang - values of pendulum not being analysed, which are needed to calculate the acceleration of the pendulum in question (used in double pendulum case)
        
        Outputs the updated position of the pendulum
        '''
        if update_method == 1:
            self.ang_acceleration[2] , self.angle, self.ang_velocity[2] =  self.update_euler(deltaT, n_pendulums, P, mass, vel, l, ang) #Calls funtions to update the pendulum object's properties.
        elif update_method == 2:
            self.ang_acceleration[2] , self.angle, self.ang_velocity[2] = self.update_cromer(deltaT, n_pendulums, P, mass, vel, l, ang)
        elif update_method == 3:                                                        #Call and run relevant update method
            self.ang_acceleration[2] , self.angle, self.ang_velocity[2] = self.update_richardson(deltaT, n_pendulums, P, mass, vel, l, ang)
        elif update_method == 4:
            self.ang_acceleration[2] , self.angle, self.ang_velocity[2] = self.update_RK(deltaT, n_pendulums, P, mass, vel, l, ang)
        
        self.tot_energy, self.kin_energy, self.pot_energy = self.calculate_E()      #Calls a fucntion to calculate total, potential and kinetic energy.
        self.flipped , self.angle = self.check_flip()

        x,y = self.pol_to_cart()                                #Converts position to cartesian coordinates
        return np.array([x,y,0], dtype = float) #Returns the new position of the pendulum object.

    def check_flip(self):
        '''
        This function determines whether the pendulum object has completed a 'flip'.
        If it has, it returns the new angle and 'yes'
        '''
        angle = self.angle
        if angle > sp.pi:
            angle -= 2* sp.pi              #Ensures: -pi < angle < pi
            return  'yes', angle
        elif angle < -sp.pi:
            angle += 2* sp.pi
            return 'yes', angle
        else:
            return 'no', angle

    def calculate_E(self):
        '''
        This function determines the potential, kinetic and total energy of the system.
        '''
        KE = (0.5) * (self.mass) * ((self.length)**2.) * ((np.linalg.norm(self.ang_velocity)**2.))
        PE = (self.mass) * 9.81 * self.length * (1 - np.cos(self.angle))      #Defines 0 PE at lowest point of swing
        E = KE + PE
        return E, KE, PE

    def damped_sho(self):   
        '''
        This function determines the acceleration of a single pendulum (including damping if present)
        '''
        if self.ang_velocity[2] >=0:
            f = 1
        else:               #Used to make damping oppose the direction of motion
            f = -1
        ang_acceleration = ( (- 9.81 / (self.length)) * np.sin(self.angle)  ) - f * self.damping_factor *self.length * np.linalg.norm(self.ang_velocity) 
        return ang_acceleration

    def update_euler(self, deltaT, n_pendulums, P, mass, vel, l, ang):
        '''
        Updates the angular velocity, angular acceleration and angle of the object using the Euler algorithm.
        The angular acceleration is updated first then angle and angular velocity.
        Returns the new angular acceleration, angle and angular velocity.
        '''
        new_acc = self.determine_acc_method(self.angle, self.ang_velocity, n_pendulums, P, mass, vel, l, ang)
        new_ang =self.angle + (self.ang_velocity[2] * deltaT)
        new_vel = self.ang_velocity[2] + (new_acc * deltaT)
        return new_acc, new_ang, new_vel
        
    def update_cromer(self, deltaT, n_pendulums, P, mass, vel, l, ang):
        '''
        Updates the angular velocity, angular acceleration and angle of the object using the Euler-Cromer algorithm.
        The angular acceleration is updated first then angular velocity. 
        The new angular velocity is used to update the angle.
        Returns the new angular acceleration, angle and angular velocity.
        '''
        new_acc = self.determine_acc_method(self.angle, self.ang_velocity, n_pendulums, P, mass, vel, l, ang)
        new_vel = self.ang_velocity[2] + new_acc * deltaT
        new_ang = self.angle + new_vel * deltaT
        return new_acc, new_ang, new_vel

    def update_richardson(self, deltaT, n_pendulums, P, mass, vel, l, ang):
        '''
        Updates the angular velocity, angular acceleration and angle of the object using the Euler-Richardson algorithm.
        The angle, angular velocity and angular acceleration are calculated for half of the time-step.
        Using the half-time-step data, the final angle, angular velocity and angular acceleration is calculated.
        Returns the new angular acceleration, angle and angular velocity.
        '''
        current_acc = self.determine_acc_method(self.angle, self.ang_velocity, n_pendulums, P, mass, vel, l, ang)
        #Find half-time-step values
        angle_mid = self.angle + self.ang_velocity[2] * (deltaT/2.0)
        ang_velocity_mid = self.ang_velocity[2] + current_acc * (deltaT/2.0)
        ang_vel_mid_vector = np.array([0.0,0.0, ang_velocity_mid])
        ang_acceleration_mid = self.determine_acc_method(angle_mid, ang_vel_mid_vector, n_pendulums, P, mass, vel, l, ang)
        
        #Using half-time-step values to calculate end point values
        new_acc = self.determine_acc_method(self.angle, self.ang_velocity, n_pendulums, P, mass, vel, l, ang)
        new_ang = self.angle + ang_velocity_mid * deltaT
        new_vel = self.ang_velocity[2] + ang_acceleration_mid * deltaT

        return new_acc, new_ang, new_vel

    def update_RK(self, deltaT, n_pendulums, P, mass, vel, l, ang):
        '''
        Updates the angular velocity, angular acceleration and angle of the object using the Runge-Kutta algorithm.
        Returns the new angular acceleration, angle and angular velocity.
        '''
        current_acc = self.determine_acc_method(self.angle, self.ang_velocity, n_pendulums, P, mass, vel, l, ang)

        #Used to store the k-values to be averaged later
        k_a = [0.,0.,0.,0.]        #Position values
        k_b = [0.,0.,0.,0.]        #Velocity values

        #Initial values
        k_a[0] = self.ang_velocity[2] * deltaT
        k_b[0] = (current_acc ) *deltaT

        #First half-time-step
        k_a[1] = (self.ang_velocity[2] + (k_b[0]/2.)) * deltaT
        ang = self.angle + (k_a[0]*0.5)
        ang_vel = np.array([0.0, 0.0, 0.0 ] , dtype = float)                                #Recalculating angular velocity from acceleration (more accurate)
        acc = self.determine_acc_method(ang, ang_vel, n_pendulums, P, mass, vel, l, ang)
        k_b[1] = acc *deltaT

        #Second half-time-step
        k_a[2] = (self.ang_velocity[2] + (k_b[1]/2.)) * deltaT
        ang = self.angle + (k_a[1]*0.5)
        ang_vel = np.array([0.0, 0.0, 0.0] , dtype = float)
        acc = self.determine_acc_method(ang, ang_vel, n_pendulums, P, mass, vel, l, ang)
        k_b[2] = acc *deltaT

        #Final full-time-step
        k_a[3] = (self.ang_velocity[2] + k_b[2]) * deltaT
        ang = self.angle + (k_a[2])
        ang_vel = np.array([0.0, 0.0, 0.0] , dtype = float)
        acc = self.determine_acc_method(ang, ang_vel, n_pendulums, P, mass, vel, l, ang)
        k_b[3] = acc *deltaT

        #Resulting values using averages for angular velocity and angle
        new_vel = self.ang_velocity[2] + ((k_b[0] + 2*k_b[1] + 2*k_b[2] + k_b[3])/6.)
        new_ang = self.angle +  ((k_a[0] + 2*k_a[1] + 2*k_a[2] + k_a[3])/6.)
        new_acc =  self.determine_acc_method(self.angle, self.ang_velocity, n_pendulums, P, mass, vel, l, ang)

        return new_acc, new_ang, new_vel

    def determine_acc_method(self, angle, ang_velocity, n_pendulums, P, mass, vel, l, ang):
        '''
        This function determines which acceleration function should be used for this system (whether it's a single or double pendulum).
        '''
        if n_pendulums == 2:    
            ang_acc = self.double_pendulum_acc(angle, ang_velocity, P, mass, vel, l, ang)
        elif n_pendulums == 1:
            ang_acc = self.damped_sho() # angle, ang_velocity)
        return ang_acc

    def double_pendulum_acc(self,angx,ang_vel, P, mass, vel, l, ang):
        '''
        This fucntion is used to determine the accleration of each mass in the double pendulum case.
        num1, num2, etc reprsent the differnt terms in the numerator
        den - denominator
        P - a variable used to detemine whether the pednulum in question if the top or bottom one.
        '''
        g = 9.81    #Accelertaion due to gravity

        if P == 'T':
            #Calculate numerator terms
            num1 = -g*(2.*self.mass + mass)*np.sin(angx)
            num2 = -mass*g*np.sin(angx - 2.*ang)
            num3 = -2.*mass*np.sin(angx - ang)
            num4 = (vel**2. * l) + (  (ang_vel[2])**2. *self.length * np.cos(angx - ang)  )
            #Calculate numerator, denominator and acceleration
            num = num1 + num2 +(num3*num4)
            den = self.length *( 2.*self.mass + mass -  mass*np.cos(2.*angx - 2.*ang) )
            acc = num/den
        elif P == 'B':
            #Calculate numerator terms
            num1 = 2.*np.sin(ang - angx)
            num2 = vel**2. * l * (mass +self.mass)
            num3 = g * (mass + self.mass) * np.cos(ang)
            num4 = (ang_vel[2]**2.) * self.length * self.mass *np.cos(ang - angx)
            #Calculate numerator, denominator and acceleration
            num = num1*(num2+num3+num4)
            den = self.length * (2. * mass + self.mass - self.mass * np.cos( 2.*ang - 2.*angx))
            acc = num/den
        return acc
