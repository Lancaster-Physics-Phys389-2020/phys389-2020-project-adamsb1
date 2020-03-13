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