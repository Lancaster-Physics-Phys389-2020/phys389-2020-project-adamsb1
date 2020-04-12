import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

data = pd.read_pickle(r'Pendulum_testing_06_04.csv')
data1 = pd.read_pickle(r'Pendulum_testing2_06_04.csv')
plt.plot([data['position'][i][0] for i in range(0,1000) ], [data['position'][i][1] for i in range(0,1000) ] , 'blue', label = 'Total Energy')
plt.plot([data1['position'][i][0] for i in range(0,1000) ], [data1['position'][i][1] for i in range(0,1000) ] , 'red', label = 'Total Energy1')
plt.show()







