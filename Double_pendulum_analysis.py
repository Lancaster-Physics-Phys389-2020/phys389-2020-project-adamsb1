import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.animation as animation




pen_1 = pd.read_pickle(r'Pendulum_double_sml.csv')
pen_2 = pd.read_pickle(r'Pendulum_double_sml_2.csv')


plt.plot([pen_1['position'][i][0] for i in range(len(pen_1['position']))], [pen_1['position'][i][1] for i in range(len(pen_1['position']))], 'red', label = 'position 1')
plt.plot([pen_2['position'][i][0] for i in range(len(pen_2['position']))], [pen_2['position'][i][1] for i in range(len(pen_2['position']))], 'blue', label = 'position 2')


plt.legend()
plt.show()


