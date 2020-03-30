

##############
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
###############


###############
#define ticks

################




#################
#import data
euler_std = pd.read_pickle(r'Pendulum_Euler_std.csv')
euler_01 = pd.read_pickle(r'Pendulum_Euler_0.01.csv')

cromer_std = pd.read_pickle(r'Pendulum_Cromer_std.csv')
cromer_01 = pd.read_pickle(r'Pendulum_Cromer_0.01.csv')

richardson_std = pd.read_pickle(r'Pendulum_Richardson_std.csv')
richardson_01 = pd.read_pickle(r'Pendulum_Richardson_0.01.csv')

rk_std = pd.read_pickle(r'Pendulum_RK_std.csv')
rk_005 = pd.read_pickle(r'Pendulum_RK_0.005.csv')
rk_01 = pd.read_pickle(r'Pendulum_RK_0.01.csv')
rk_05 = pd.read_pickle(r'Pendulum_RK_0.05.csv')
rk_1 = pd.read_pickle(r'Pendulum_RK_0.1.csv')
rk_25 = pd.read_pickle(r'Pendulum_RK_0.25.csv')
rk_5 = pd.read_pickle(r'Pendulum_RK_0.5.csv')

################

length = len(euler_std['time'])

print(length)
print('euler before:' ,  euler_std['tot_energy'][0])
print('euler after:' ,  euler_std['tot_energy'][100000])
print()

print('c before:' ,  cromer_std['tot_energy'][0])
print('c after:' ,  cromer_std['tot_energy'][100000])
print()

print('er before:' ,  richardson_std['tot_energy'][0])
print('er before:' ,  richardson_std['tot_energy'][100000])
print()

print ( (19.619999999999987- 19.61999999759978)/500)

print('rk before:' ,  rk_std['tot_energy'][0])
print('rk before:' ,  rk_std['tot_energy'][100000]) 
input()







################
#Comparison of error in energy

#Euler
y1 = euler_std['tot_energy'] / euler_std['tot_energy'][0]
y1 = np.log10(y1)
x1 = euler_std['time']

#Cromer
y2 =cromer_std['tot_energy'] / cromer_std['tot_energy'][0]
y2 = np.log(y2)
x2 = cromer_std['time']

#Richardon
y3 = richardson_std['tot_energy'] / richardson_std['tot_energy'][0]
y3 = np.log(y3)
x3 = richardson_std['time']

#Runge-Kutta
y4 = rk_std['tot_energy'] / rk_std['tot_energy'][0]
y4 = np.log10(y4)
x4 = rk_std['time']

##############


###############
#comparison of all methods
plt.figure(figsize = [8.0,8.0])
plt.plot(x1,y1, 'blue', label = 'Euler')
plt.plot(x2,y2, 'green', label = 'Euler-Cromer')
plt.plot(x3,y3, 'maroon', label = 'Euler-Richardson')
plt.plot(x4,y4, 'yellow', label = 'Runge-Kutta')

plt.ylabel('log(Error in total energy [J])', size =20)
plt.xlabel('Time [s]', size = 20)
plt.legend(prop = {'size':14})
plt.savefig('Method_comparison8.pdf')

################



###############
#Euler
plt.figure(figsize = [8.0,8.0])
plt.plot(x1,y1, 'blue', label = 'Euler')
plt.ylabel('log(Error in total energy [J])', size =20)
plt.xlabel('Time [s]', size =20)
plt.legend(prop = {'size':14})
plt.savefig('Euler_energy_err3.pdf')
plt.close()
################

###############
#Cromer
plt.figure(figsize = [8.0,8.0])
plt.plot(x2,y2, 'green', label = 'Euler-Cromer')
plt.ylabel('log(Error in total energy [J])', size =20)
plt.xlabel('Time [s]', size =20)
plt.legend(prop = {'size':14})
plt.savefig('Cromer_energy_err3.pdf')
plt.close()
################

###############
#Richardson
plt.figure(figsize = [8.0,8.0])
plt.plot(x3,y3, 'maroon', label = 'Euler-Richardson')
plt.ylabel('log(Error in total energy [J])', size =20)
plt.xlabel('Time [s]', size =20)
plt.legend(prop = {'size':14})
plt.savefig('Richardson_energy_err3.pdf')
plt.close()
################

###############
#RK
plt.figure(figsize = [8.0,8.0])
plt.plot(x4,y4, 'yellow', label = 'Runge-Kutta')
plt.ylabel('log(Error in total energy [J])', size =20)
plt.xlabel('Time [s]', size =20)
plt.legend(prop = {'size':14})
plt.savefig('RK_energy_err3.pdf')
plt.close()
################

################
#Comparing damped system


############
plt.figure(figsize = [8.0,8.0])
plt.plot(euler_01['time'],euler_01['tot_energy'], 'blue', label = 'Euler')
plt.plot(cromer_01['time'],cromer_01['tot_energy'], 'green', label = 'Euler-Cromer')
plt.plot(richardson_01['time'],richardson_01['tot_energy'], 'maroon', label = 'Euler-Richardson')
plt.plot(rk_01['time'],rk_01['tot_energy'], 'yellow', label = 'Runge-Kutta')

plt.ylabel('Total energy [J]', size =20)
plt.xlabel('Time [s]', size =20)
plt.legend(prop = {'size':14})
plt.savefig('Method_damped_comparison3.pdf')
plt.close()
############

#######
#RK
plt.figure(figsize = [8.0,8.0])
plt.plot(rk_01['time'],rk_01['tot_energy'], 'yellow', label = 'Runge-Kutta')
plt.ylabel('Total energy [J]', size =20)
plt.xlabel('Time [s]', size =20)
plt.legend(prop = {'size':14})
plt.savefig('RK_energy_damped3.pdf')
plt.close()

#Richardson
plt.figure(figsize = [8.0,8.0])
plt.plot(richardson_01['time'],richardson_01['tot_energy'], 'maroon', label = 'Euler-Richardson')
plt.ylabel('Total energy [J]', size =20)
plt.xlabel('Time [s]', size =20)
plt.legend(prop = {'size':14})
plt.savefig('Richardson_energy_damped3.pdf')
plt.close()

#Cromer
plt.figure(figsize = [8.0,8.0])
plt.plot(cromer_01['time'],cromer_01['tot_energy'], 'green', label = 'Euler-Cromer')
plt.ylabel('Total energy [J]', size =20)
plt.xlabel('Time [s]', size =20)
plt.legend(prop = {'size':14})
plt.savefig('Cromer_energy_damped3.pdf')
plt.close()

#euler
plt.figure(figsize = [8.0,8.0])
plt.plot(euler_01['time'],euler_01['tot_energy'], 'blue', label = 'Euler')
plt.ylabel('Total energy [J]', size =20)
plt.xlabel('Time [s]', size =20)
plt.legend(prop = {'size':14})
plt.savefig('euler_energy_damped3.pdf')
plt.close()

#########


##############
#compare amount of damping

plt.figure(figsize = [8.0,8.0])
plt.plot(rk_005['time'],rk_005['tot_energy'], 'red', label = 'Damping: 0.005')
plt.plot(rk_01['time'],rk_01['tot_energy'], 'blue', label = 'Damping: 0.01')
plt.plot(rk_05['time'],rk_05['tot_energy'], 'yellow', label = 'Damping: 0.05')
plt.plot(rk_1['time'],rk_1['tot_energy'], 'green', label = 'Damping: 0.1')
plt.plot(rk_25['time'],rk_25['tot_energy'], 'c', label = 'Damping: 0.25')
plt.plot(rk_5['time'],rk_5['tot_energy'], 'k', label = 'Damping: 0.5')

plt.ylabel('Total energy [J]', size =20)
plt.xlabel('Time [s]', size =20)
plt.legend(prop = {'size':14})
plt.savefig('RK_energy_damped_compare3.pdf')
plt.close()





