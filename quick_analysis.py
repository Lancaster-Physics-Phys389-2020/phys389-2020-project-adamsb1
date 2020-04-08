import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

data = pd.read_pickle(r'Pendulum_testing_06_04.csv')
plt.plot([data['position'][i][0] for i in range(0,10000) ], [data['position'][i][1] for i in range(0,10000) ] , 'blue', label = 'Total Energy')

plt.show()







