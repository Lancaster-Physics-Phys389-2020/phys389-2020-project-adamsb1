import pytest
import scipy.constants
from Pendulum2 import Pendulum
from Double_Pendulum import DoublePendulum
import numpy as np
import math
import copy

##########
#Testing Pendulum2.py
##########

@pytest.mark.parametrize("test_input, expected1, expected2", [(Pendulum(position = [0,1,0]),1.0,scipy.constants.pi),(Pendulum(position = [0,-1,0]), 1.0,0.0), (Pendulum(position = [3,-3,0]), 4.242640687119285, scipy.constants.pi / 4), (Pendulum(position = [-2,6,0]), 40.**0.5 ,-2.819842099193151) ])
def test_cart_to_pol_position(test_input, expected1, expected2):
    assert Pendulum.cart_to_pol_position(test_input)[1] == expected2
    assert Pendulum.cart_to_pol_position(test_input)[0] == expected1

@pytest.mark.parametrize("test_input, expected1, expected2", [(Pendulum(angle = 0., length = 1.,  origin_point = [0.,0.,0.]), 0, -1),(Pendulum(angle = scipy.constants.pi/2, length = 2.,  origin_point = [0.,0.,0.]), 2, 0) , (Pendulum(angle = scipy.constants.pi/6, length = 5,  origin_point = [0.,0.,0.]), 5/2, - (5*(3**0.5))/2 ) , (Pendulum(angle = -5*scipy.constants.pi/6, length = 5,  origin_point = [0.,0.,0.]), -5/2,  (5*(3**0.5))/2 ) ])
def test_pol_to_cart(test_input, expected1, expected2):
    assert math.isclose(Pendulum.pol_to_cart(test_input)[1],expected2) == True
    assert math.isclose(Pendulum.pol_to_cart(test_input)[0],expected1) == True

@pytest.mark.parametrize("test_input, expected1, expected2", [(Pendulum( position = [3.,4.,0.] , origin_point = [0.,0.,0.] ) , 3., 4.), (Pendulum( position = [3,4,0] , origin_point = [0.,0.,0.] ) , 3., 4.) , (Pendulum( position = [3.,4.,0.] , origin_point = [0,0,0] ) , 3., 4.) , (Pendulum( position = [3.,4.,0.] , origin_point = [4.,5.,0.] ) , -1., -1.)  ])
def test_delta_values(test_input, expected1, expected2):
    assert Pendulum.delta_values(test_input)[1] == expected2
    assert Pendulum.delta_values(test_input)[0] == expected1

@pytest.mark.parametrize("test_input, expected1, expected2", [ (Pendulum( angle = 0.), 'no', 0) , (Pendulum( angle = scipy.constants.pi), 'no', scipy.constants.pi) , (Pendulum(angle = -4), 'yes', 2.2831853071795862) , (Pendulum(angle = 4), 'yes', -2.2831853071795862)            ]   )
def test_check_flip(test_input, expected1, expected2):
    assert Pendulum.check_flip(test_input)[0] == expected1
    assert Pendulum.check_flip(test_input)[1] == expected2

@pytest.mark.parametrize("test_input, expected1, expected2, expected3", [ (Pendulum( mass = 1.0, length = 1.0, ang_velocity = np.array([0.,0.,1.]), angle = scipy.constants.pi /2), 10.31, 0.5, 9.81  ) ,(Pendulum( mass = 1, length = 1, ang_velocity = np.array([0,0,1]), angle = -scipy.constants.pi/2), 10.31, 0.5, 9.81  ) , (Pendulum( mass = 1.0, length = 1.0, ang_velocity = np.array([0.,0.,1.]), angle = 0.), 0.5, 0.5, 0  ) ,  (Pendulum( mass = 1.0, length = 1.0, ang_velocity = np.array([0.,0.,0.]), angle = scipy.constants.pi), 19.62, 0., 19.62  )     ])
def test_calculate_E(test_input, expected1, expected2, expected3):
    assert math.isclose(Pendulum.calculate_E(test_input)[0],expected1) == True
    assert math.isclose(Pendulum.calculate_E(test_input)[1],expected2) == True
    assert math.isclose(Pendulum.calculate_E(test_input)[2],expected3) == True

@pytest.mark.parametrize("test_input, expected1", [ (Pendulum( ang_velocity = [0.,0.,0.], angle = 0. , length = 1. , damping_factor = 0.  ),0.)  , (Pendulum( ang_velocity = [0,0,0], angle = 0 , length = 1 , damping_factor = 0  ),0)  , (Pendulum( ang_velocity = [0.,0.,3.], angle = 1. , length = 1. , damping_factor = 0.  ),-8.254830361)  , (Pendulum( ang_velocity = [0.,0.,3.], angle = -1. , length = 1. , damping_factor = 0.  ),8.254830361)  , (Pendulum( ang_velocity = [0.,0.,3.], angle = 1. , length = 1. , damping_factor = 0.05  ),-8.404830361) , (Pendulum( ang_velocity = [0.,0.,3.], angle = -1. , length = 1. , damping_factor = 0.05  ),8.104830361)                     ])
def test_damped_sho(test_input, expected1):
    assert math.isclose(Pendulum.damped_sho(test_input),expected1) == True

@pytest.mark.parametrize("test_input, angx, ang_vel, P, mass, vel, l, ang, expected1", [   (Pendulum(mass = 1.0, angle = 1.0 , length = 1.0), 1.0, [0., 0., 1.0], 'T', 1.0, 1.0, 1.0, 1.0 , -8.254830361 ) , (Pendulum(mass = 1, angle = 1, length = 1), 1, [0, 0, 1], 'B', 1, 1, 1, 1 , 0 ),  (Pendulum(mass = 1., angle = 1., length = 1.), 1., [0., 0., 1.], 'B', 1., 1., 1., -2. , 0.9899694076 )      ])
def test_double_pendulum_acc(test_input, angx, ang_vel, P, mass, vel, l, ang, expected1):
    print(Pendulum.double_pendulum_acc(test_input, angx, ang_vel, P, mass, vel, l , ang))
    assert math.isclose(Pendulum.double_pendulum_acc(test_input, angx, ang_vel, P, mass, vel, l , ang),expected1) == True

@pytest.mark.parametrize("test_input, deltaT, n_pendulums, P, mass, vel, l, ang, expected1, expected2, expected3", [   (Pendulum( angle = 0.5, length = 1.0, ang_velocity = [0.0,0.0,3.0]),0.05,1,'',0.0, 0.0,0.0,0.0, -4.703164534, 0.65, 2.764841773) , (Pendulum( angle = 1, length = 1, ang_velocity = [0,0,3]),0.05,1,'',0.0, 0.0,0.0,0.0, -8.254830361, 1.15, 2.587258482), ( Pendulum( angle = 1.0, length = 1.0, ang_velocity = [0,0,3], mass = 1.0),0.05, 2, 'T', 1.0, 0.0, 1.0, 1.0, -8.25483036, 1.15, 2.587258482    )          ]      ) 
def test_update_euler(test_input, deltaT, n_pendulums, P, mass, vel, l, ang, expected1, expected2, expected3):
    acc, ang, vel = test_input.update_euler(deltaT, n_pendulums, P, mass, vel, l , ang)
    assert math.isclose(acc,expected1) == True
    assert math.isclose(ang,expected2) == True
    assert math.isclose(vel,expected3) == True
    
@pytest.mark.parametrize("test_input, deltaT, n_pendulums, P, mass, vel, l, ang, expected1, expected2, expected3", [   (Pendulum( angle = 0.5, length = 1.0, ang_velocity = [0.0,0.0,3.0]),0.05,1,'',0.0, 0.0,0.0,0.0, -4.703164534, 0.6382420887, 2.764841773) , (Pendulum( angle = 1, length = 1, ang_velocity = [0,0,3]),0.05,1,'',0.0, 0.0,0.0,0.0, -8.254830361, 1.129362924, 2.587258482), ( Pendulum( angle = 1.0, length = 1.0, ang_velocity = [0,0,3], mass = 1.0),0.05, 2, 'T', 1.0, 0.0, 1.0, 1.0, -8.25483036, 1.129362924, 2.587258482    )          ]      ) 
def test_update_cromer(test_input, deltaT, n_pendulums, P, mass, vel, l, ang, expected1, expected2, expected3):
    acc, ang, vel = test_input.update_cromer(deltaT, n_pendulums, P, mass, vel, l , ang)
    assert math.isclose(acc,expected1) == True
    assert math.isclose(ang,expected2) == True
    assert math.isclose(vel,expected3) == True

@pytest.mark.parametrize("test_input, deltaT, n_pendulums, P, mass, vel, l, ang, expected1, expected2, expected3", [   (Pendulum( angle = 0.5, length = 1.0, ang_velocity = [0.0,0.0,3.0]),0.05,1,'',0.0, 0.0,0.0,0.0, -4.703164534, 0.644121044, 2.764841773) , (Pendulum( angle = 1, length = 1, ang_velocity = [0,0,3]),0.05,1,'',0.0, 0.0,0.0,0.0, -8.254830361, 1.139681462, 2.587258482), ( Pendulum( angle = 1.0, length = 1.0, ang_velocity = [0,0,3], mass = 1.0),0.05, 2, 'T', 1.0, 0.0, 1.0, 1.0, -8.25483036, 1.139681462048,2.52222897500    )          ]      ) 
def test_update_richardson(test_input, deltaT, n_pendulums, P, mass, vel, l, ang, expected1, expected2, expected3):
    acc, ang, vel = test_input.update_richardson(deltaT, n_pendulums, P, mass, vel, l , ang)
    assert math.isclose(acc,expected1) == True
    assert math.isclose(ang,expected2) == True
    assert math.isclose(vel,expected3) == True

@pytest.mark.parametrize("test_input, deltaT, n_pendulums, P, mass, vel, l, ang, expected1, expected2, expected3", [   (Pendulum( angle = 0.5, length = 1.0, ang_velocity = [0.0,0.0,3.0]),0.05,1,'',0.0, 0.0,0.0,0.0, -4.703164534, 0.644121044, 2.764841773) , (Pendulum( angle = 1, length = 1, ang_velocity = [0,0,3]),0.05,1,'',0.0, 0.0,0.0,0.0, -8.254830361, 1.139681462, 2.587258482), ( Pendulum( angle = 1.0, length = 1.0, ang_velocity = [0,0,3], mass = 1.0),0.05, 2, 'T', 1.0, 0.0, 1.0, 1.0, -6.32676751734,1.1393799181,2.56973304592    )          ]      ) 
def test_update_RK(test_input, deltaT, n_pendulums, P, mass, vel, l, ang, expected1, expected2, expected3):
    acc, ang, vel = test_input.update_RK(deltaT, n_pendulums, P, mass, vel, l , ang)
    assert math.isclose(acc,expected1) == True
    assert math.isclose(ang,expected2) == True
    assert math.isclose(vel,expected3) == True

@pytest.mark.parametrize("test_input, n_pendulums, P, mass, vel, l, ang, expected1", [   (Pendulum( angle = 0.5, length = 1.0, ang_velocity = [0.0,0.0,3.0], mass = 1.0),1,'',0.0, 0.0,0.0,0.0, -4.703164534) , (Pendulum( angle = 1, length = 1, ang_velocity = [0,0,3], mass = 1),1,'',0.0, 0.0,0.0,0.0, -8.254830361), ( Pendulum( angle = 1.0, length = 1.0, ang_velocity = [0,0,3], mass = 1.0), 2, 'T', 1.0, 0.0, 1.0, 1.0, -8.2548303609654  )          ]      ) 
def test_determine_acc_method(test_input, n_pendulums, P, mass, vel, l, ang, expected1):
    acc = test_input.determine_acc_method(test_input.angle, test_input.ang_velocity, n_pendulums, P, mass, vel, l , ang)
    assert math.isclose(acc,expected1) == True

@pytest.mark.parametrize("test_input, deltaT, update_method, n_pendulums, P, mass, vel, l, ang, flip, expected1, expected2", [   (Pendulum( position = [1.,1.,0.], length = 1.0, mass = 1.0), 0.05, 1, 1,'',0.0, 0.0,0.0,0.0,'', 1.02422181880,0.9751767357) ,  (Pendulum( position = [1,1,0], length = 1, mass = 1), 0.05, 2, 1,'',0.0, 0.0,0.0,0.0,'', 1.071077553773,0.9234678520674), (Pendulum( position = [0.00,-1.00,0.], length = 1., mass = 1.), 0.001, 4, 1,'',0.0, 0.0,0.0,0.0,'', 0.000,-1.000)        ]      ) 
def test_update(test_input,deltaT, update_method, n_pendulums, P, mass, vel, l, ang,flip, expected1, expected2):

    pos = test_input.update(deltaT, update_method, n_pendulums, P, mass, vel, l , ang, flip)
    print(pos)
    assert math.isclose(pos[0],expected1,rel_tol = 1e-01, abs_tol = 0.01) == True
    assert math.isclose(pos[1],expected2,rel_tol = 1e-01, abs_tol = 0.01) == True


##########
#Testing Doubple_Pendulum.py
##########


#Single pendulum
@pytest.mark.parametrize("test_input, n_pendulums, deltaT, method, flip, expected1, expected2, expected3, expected4",[ ([ DoublePendulum([ (np.array([np.array([1.,1.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, 0., 1., [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], 0.0, 0.0, 0.0, 0.0])) ]) , DoublePendulum([(np.array([np.array([1,1,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, 0., 1., [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], 0.0, 0.0, 0.0, 0.0]) )    ])  ] , 1, 0.05,2,'', 1.036246453364,0.962389363973,1.036246453364,0.962389363973) ])
def test_call_update(test_input, n_pendulums, deltaT, method, flip, expected1, expected2, expected3, expected4):
    print(test_input)
    new_pos1 = test_input[0].call_update( n_pendulums, deltaT, method, flip)
    new_pos2 = test_input[1].call_update( n_pendulums, deltaT, method, flip)
    assert math.isclose(new_pos1[0][0],expected1) == True
    assert math.isclose(new_pos1[0][1],expected2) == True
    assert math.isclose(new_pos2[0][0],expected3) == True
    assert math.isclose(new_pos2[0][1],expected4) == True

#######
#Setting conditions for testing
pendulum1 = np.array([np.array([1.,1.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, 0., 1., [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], 0.0, 0.0, 0.0, 0.0])     
pendulum2 = np.array([ np.array([2.,2. ,0.]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, 0., 1., [0.,0.,0.], [0.,0.,0.], [1.,1.,0.], 0.0, 0.0, 0.0, 0.0])
listofobjects = [pendulum1, pendulum2]      
pendulums = DoublePendulum(listofobjects)
#######

#Double pendulum 
@pytest.mark.parametrize("test_input, n_pendulums, deltaT, method, flip, expected1, expected2, expected3, expected4",[ (pendulums, 2,0.05,4,'',1.024331293828,0.975061741882,1.99985754943796,2.00014243027)] )
def test_call_update_double(test_input, n_pendulums, deltaT, method, flip, expected1, expected2, expected3, expected4):
    new_pos1 = test_input.call_update( n_pendulums, deltaT, method, flip)
    assert math.isclose(new_pos1[0][0],expected1) == True
    assert math.isclose(new_pos1[0][1],expected2) == True
    assert math.isclose(new_pos1[1][0],expected3) == True
    assert math.isclose(new_pos1[1][1],expected4) == True

@pytest.mark.parametrize("test_input, i, expected1, expected2, expected3, expected4, expected5",[ ( DoublePendulum([ np.array([np.array([0.,0.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1., 0.5, 1., [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], 0.0, 0.0, 0.0, 0.0 ])]),1  , 1., 0.0, 1., 0.5, 'B'   ) , ( DoublePendulum([ np.array([np.array([0.,0.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, 0.5, 1, [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], 0.0, 0.0, 0.0, 0.0 ])]),1  , 1., 0.0, 1., 0.5, 'B'   ), (pendulums, 0, 1., 0.0, 1.41421356237, 2.35633693061, 'T') ] )
def test_second_pendulum_data(test_input,i,expected1,expected2,expected3,expected4,expected5):
    output_data = test_input.second_pendulum_data(i)
    print(test_input)
    assert math.isclose(output_data[0],expected1) == True
    assert math.isclose(output_data[1],expected2, abs_tol = 0.01) == True
    assert math.isclose(output_data[2],expected3) == True
    assert math.isclose(output_data[3],expected4) == True
    assert output_data[4]== expected5

#######
#Setting conditions for testing
pendulum1 = np.array([np.array([1.,1.,0]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, 0., 1., [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], 0.0, 0.0, 0.0, 0.0])     
pendulum2 = np.array([ np.array([2.,2. ,0.]),np.array([0.,0,0]),np.array([0,0,0]),'ball', 1, 0., 1., [0.,0.,0.], [0.,0.,0.], [1.,1.,0.], 0.0, 0.0, 0.0, 0.0])
listofobjects = [pendulum1, pendulum2]      
pendulums = DoublePendulum(listofobjects)
list1 = [pendulum1]
pendulums1 = DoublePendulum(list1)
#######

#Single Pendulum
@pytest.mark.parametrize("test_input, duration, deltaT, method, time_analysis, expected1, expected2", [ (pendulums1, 0.005, 0.005, 2, 'N',1.,1.) ])
def test_run_simulation(test_input, duration, deltaT, method, time_analysis, expected1, expected2):
    output_data = test_input.run_simulation(duration, deltaT,method, time_analysis)
    print(output_data)
    assert math.isclose(output_data[0][0][1][0],expected1, abs_tol = 0.01) == True
    assert math.isclose(output_data[0][0][1][1],expected2, abs_tol = 0.01) == True

#Double Pendulum
@pytest.mark.parametrize("test_input, duration, deltaT, method, time_analysis, expected1", [ (pendulums,0.1, 0.005, 2, 'Y',0.0) ])
def test_run_simulation_double(test_input, duration, deltaT, method, time_analysis, expected1):
    output_data = test_input.run_simulation(duration, deltaT,method, time_analysis)
    print(output_data)
    assert math.isclose(output_data[0],expected1) == True

pytest.main()