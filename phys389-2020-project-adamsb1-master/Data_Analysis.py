import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

#data = pd.read_pickle(r'Euler_update_r.csv')
#print(data['kin_energy'])

#data.plot(x = 'time', y = 'position', kind = 'scatter')
#print([data['position'][i][1] for i in range(len(data['position']))])
#plt.plot([data['position'][i][0] for i in range(len(data['position']))], [data['position'][i][1] for i in range(len(data['position']))], 'red', label = 'position')

#plt.plot( data['time'],data['kin_energy'], 'blue', label = 'Ke')
#plt.plot( data['time'],data['pot_energy'], 'red', label = 'Pe')
#plt.plot( data['time'],data['tot_energy'], 'black', label = 'tot')


#plt.plot(data['time'], data['angular_acceleration'], 'blue', label = 'alpha')
#plt.legend()
#plt.show()


data1 = pd.read_pickle(r'Pendulum_RK.csv')
#data2 = pd.read_pickle(r'Pendulum_e.csv')
#data3 = pd.read_pickle(r'Pendulum_c.csv')

plt.plot([data1['position'][i][0] for i in range(len(data1['position']))], [data1['position'][i][1] for i in range(len(data1['position']))], 'red', label = 'position r')
#plt.plot([data2['position'][i][0] for i in range(len(data2['position']))], [data2['position'][i][1] for i in range(len(data2['position']))], 'blue', label = 'position e')
#plt.plot([data3['position'][i][0] for i in range(len(data3['position']))], [data3['position'][i][1] for i in range(len(data3['position']))], 'green', label = 'position c')
plt.legend()
plt.show()

plt.plot( data1['time'],data1['tot_energy'] / data1['tot_energy'][0], 'blue', label = 'euler')
plt.legend()
plt.show()

#plt.plot(data1['time'],data1['tot_energy']/ data1['tot_energy'][0], 'red')

plt.plot( data2['time'],data2['tot_energy'] / data2['tot_energy'][0], 'blue', label = 'euler')
plt.plot( data3['time'],data3['tot_energy'] /data3['tot_energy'][0], 'red', label = 'cromer')
plt.plot( data1['time'],data1['tot_energy'] /data1['tot_energy'][0], 'black', label = 'richardson')
plt.legend()
plt.show()

data1 = pd.read_pickle(r'Pendulum_r_0.1.csv')
data2 = pd.read_pickle(r'Pendulum_e_0.1.csv')
data3 = pd.read_pickle(r'Pendulum_c_0.1.csv')

plt.plot( data2['time'],data2['tot_energy'] , 'blue', label = 'euler')
plt.plot( data3['time'],data3['tot_energy'] , 'red', label = 'cromer')
plt.plot( data1['time'],data1['tot_energy'], 'black', label = 'richardson')
plt.legend()
plt.show()