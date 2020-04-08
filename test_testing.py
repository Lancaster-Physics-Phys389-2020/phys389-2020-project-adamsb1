'''
to test:
Pendulum 2:

    cart_to_pol_position

        (+,+), (+,-), (-,+), (-,-)       (F)
        (0,0)                          (B)
        (int,int)                   (WDT)
    
    
    delta values

        attempt two different arrays, e.g 2,3 and 4,5   (F)
        try same value ==0                              (F)
        attempt one integer, one float                  (WDT) 
    
    
    update


    calculate_E

        angle = 0    (F)
        input basic values   (F)
        some ints some floats (WDT)
        value = 0       (B)
    
    
    pol_to_cart

        angles in all 4 quadrants?       (F)
        try L = 0               (B)
        integer    (WDT)
    
    
    damped_sho
        damping factor = 0          (F)
        damping factor = 0.324         (F)
        damping factor = int            (F / WDT)


tests:
    boundary  (B)
    normal      (F)
    wrong type data, e.g. int instead of float  (WDT)





'''


import pytest

import scipy.constants

from Pendulum2 import Pendulum

import numpy as np

import math

@pytest.mark.parametrize("test_input, expected1, expected2", [(Pendulum(position = [0,1,0]),1.0,scipy.constants.pi),(Pendulum(position = [0,-1,0]), 1.0,0.0), (Pendulum(position = [3,-3,0]), 4.242640687119285, scipy.constants.pi / 4), (Pendulum(position = [-2,6,0]), 40.**0.5 ,-2.819842099193151) ])
def test_cart_to_pol_position(test_input, expected1, expected2):
    assert Pendulum.cart_to_pol_position(test_input)[1] == expected2
    assert Pendulum.cart_to_pol_position(test_input)[0] == expected1


@pytest.mark.parametrize("test_input, expected1, expected2", [(Pendulum(angle = 0., length = 1.,  origin_point = [0.,0.,0.]), 0, -1),(Pendulum(angle = scipy.constants.pi/2, length = 2.,  origin_point = [0.,0.,0.]), 2, 0) , (Pendulum(angle = scipy.constants.pi/6, length = 5,  origin_point = [0.,0.,0.]), 5/2, - (5*(3**0.5))/2 ) , (Pendulum(angle = -5*scipy.constants.pi/6, length = 5,  origin_point = [0.,0.,0.]), -5/2,  (5*(3**0.5))/2 ) ])
def test_pol_to_cart(test_input, expected1, expected2):
    assert math.isclose(Pendulum.pol_to_cart(test_input)[1],expected2) == True
    assert math.isclose(Pendulum.pol_to_cart(test_input)[0],expected1) == True

#math.isclose(Pendulum.pol_to_cart(test_input)[1],expected2) == True


@pytest.mark.parametrize("test_input, expected1, expected2", [(Pendulum( position = [3.,4.,0.] , origin_point = [0.,0.,0.] ) , 3., 4.), (Pendulum( position = [3,4,0] , origin_point = [0.,0.,0.] ) , 3., 4.) , (Pendulum( position = [3.,4.,0.] , origin_point = [0,0,0] ) , 3., 4.) , (Pendulum( position = [3.,4.,0.] , origin_point = [4.,5.,0.] ) , -1., -1.)  ])
def test_delta_values(test_input, expected1, expected2):
    assert Pendulum.delta_values(test_input)[1] == expected2
    assert Pendulum.delta_values(test_input)[0] == expected1

#Update cannot be tested as it is a method not a function.

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

#   @pytest.mark.parametrize("test_input, expected1", [ (n_pendulums = 1, 2)            ])
#def test_determine_acc_method(test_input):
 #   assert Pendulum.determine_acc_method(test_input) == expected1


@pytest.mark.parametrize("test_input, angx, ang_vel, P, mass, vel, l, ang, expected1", [   (Pendulum(mass = 1.0, angle = 1.0 , length = 1.0), 1.0, [0., 0., 1.0], 'T', 1.0, 1.0, 1.0, 1.0 , -8.254830361 ) , (Pendulum(mass = 1, angle = 1, length = 1), 1, [0, 0, 1], 'B', 1, 1, 1, 1 , 0 ),  (Pendulum(mass = 1., angle = 1., length = 1.), 1., [0., 0., 1.], 'B', 1., 1., 1., -2. , 0.9899694076 )      ])
def test_double_pendulum_acc(test_input, angx, ang_vel, P, mass, vel, l, ang, expected1):
    print(Pendulum.double_pendulum_acc(test_input, angx, ang_vel, P, mass, vel, l , ang))
    assert math.isclose(Pendulum.double_pendulum_acc(test_input, angx, ang_vel, P, mass, vel, l , ang),expected1) == True




'''
#@pytest.mark.parametrize("test_input, deltaT, expected", [("Tether(np.array([0,0,0]),np.array([0,0,0]),np.array([0,0,0]),'head', 1, scipy.constants.pi/2, 1., 0., 0. )", 0.1, 0.1)])

#def test_update_alpha(test_input, deltaT, expected):

#    assert Tether.update_omega(test_input, deltaT) == expected



@pytest.mark.parametrize("test_input, expected", [(Tether([0,1,0]), scipy.constants.pi), (Tether([1,0,0]), scipy.constants.pi/2), (Tether([-1,0,0]), 3*scipy.constants.pi/2), (Tether([0,-1,0]),0)])

def test_set_theta(test_input, expected):

    assert Tether.set_theta(test_input) == expected



@pytest.mark.parametrize("test_input, expected", [(Tether([0,1,0]), 1.),(Tether([3,4,0]), 5.), (Tether([3,-4,0]), 5.), (Tether([2.5, 6.5, 0]), 6.96419413859206)  ] )

def test_set_length(test_input, expected):

    assert Tether.set_length(test_input) == expected



@pytest.mark.parametrize("test_input, expected", [(Tether(Position=[0,1,0], Velocity=[0,0,0], Length = 1), [0,0,0]),(Tether(Position=[3,4,0], Velocity=[0,1,0], Length = 5.), [0,0,0.12]), (Tether(Position=[0,0,0], Velocity=[0,1,0], Length = 0.), [0,0,0])])

def test_set_omega(test_input, expected):

        assert np.allclose(Tether.set_omega(test_input), expected, rtol = 1E-10)



@pytest.mark.parametrize("test_input, expected", [((Tether(Position=[0,0,0], Theta=scipy.constants.pi/2)), [0.,0.,0.]), ((Tether(Position=[0,1000.,0], Theta=scipy.constants.pi)), [0.,0.,0.])] )

def test_update_alpha(test_input, expected):

    assert np.allclose(Tether.update_alpha(test_input, 0.1), expected, rtol = 1E-10)



@pytest.mark.parametrize("test_input, expected", [(Tether(Position = [1,0,0], Velocity=np.array([0,4,0]), alpha=np.array([0,0,5])), [0,0,4.5]), (Tether(Position = [1,0,0]), [0,0,0])])

def test_update_omega(test_input, expected):

    assert np.allclose(Tether.update_omega(test_input, 0.1), expected, rtol = 1E-10)





#zero error if set at [0,1,0]



#np.allclose

'''
pytest.main()