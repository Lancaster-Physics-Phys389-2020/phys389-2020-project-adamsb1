import numpy as np
import scipy.constants as sp
def cart_to_pol():
    x,y = delta_values()
    rho = np.sqrt(x**2. + y**2.)
    phi = np.arctan2(y,x) + (sp.pi/2)
    if phi> sp.pi:
        phi = phi -sp.pi * 2. 

    return rho, phi

def delta_values():
    delta_x = position[0] - origin_point[0]
    delta_y = position[1] - origin_point[1]
    return delta_x, delta_y

origin_point = [0.,-5.]
position = [0.,-10.]

def pol_to_cart(rho1, phi1):
    delta_x = rho1 * np.cos(phi1 -sp.pi/2)
    delta_y = rho1 * np.sin(phi1 - sp.pi/2)

    return delta_x , delta_y



x , y = delta_values()
rho, phi = cart_to_pol()

print('rho', rho)
print('phi', phi)



x,y = pol_to_cart(5, 2.617993878)
print('x', x - origin_point[0])
print('y', y - origin_point[1])


mass = 1.0
length = 1.0
ang_velocity = [1.,1.,0.]
print ('KE',  (0.5) * (mass) * ((length)**2.) * ((np.linalg.norm(ang_velocity)**2.))  )