import scipy.integrate as sp
import numpy as np
import matplotlib.pyplot as plt

Pk = np.linspace(0,1,100)
deltheta = np.linspace(0,np.pi,100)
plt.plot(Pk,np.arcsin(Pk))
plt.plot(Pk,np.pi - np.arcsin(Pk),ls = '--')
plt.show()
