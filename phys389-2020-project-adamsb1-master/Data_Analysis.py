import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

data = pd.read_pickle(r'Euler_update_c.csv')
print(data['kin_energy'])

#data.plot(x = 'time', y = 'position', kind = 'scatter')
#print([data['position'][i][1] for i in range(len(data['position']))])
#plt.plot([data['position'][i][0] for i in range(len(data['position']))], [data['position'][i][1] for i in range(len(data['position']))], 'red', label = 'position')

plt.plot( data['time'],data['kin_energy'], 'blue', label = 'Ke')
plt.plot( data['time'],data['pot_energy'], 'red', label = 'Pe')
plt.plot( data['time'],data['tot_energy'], 'black', label = 'tot')


#plt.plot(data['time'], data['angular_acceleration'], 'blue', label = 'alpha')
plt.legend()
plt.show()