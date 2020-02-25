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

origin_point = [0.,0.]
position = [-4.,3.]

def pol_to_cart():
    delta_x = rho * np.cos(phi -sp.pi/2)
    delta_y = rho * np.sin(phi - sp.pi/2)

    return delta_x , delta_y



x , y = delta_values()
rho, phi = cart_to_pol()

print('rho', rho)
print('phi', phi)

x,y = pol_to_cart()
print('x', x - origin_point[0])
print('y', y - origin_point[1])