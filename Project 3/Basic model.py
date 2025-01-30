import scipy.integrate as sp
import numpy as np
import matplotlib.pyplot as plt

A = np.matrix([[0,1],[1,0]])
P = [1,1]
n = 2
gamma = 0.9
kappa = 2
thetazero = [0,0,0,0]
deltatheta = 1

def dtheta1(theta , t):
    return [theta[1],
            P[0] - kappa * np.sin(theta[0] - theta[2]) - gamma * theta[1],
            theta[3],
            P[1] - kappa * np.sin(theta[2] - theta[0]) - gamma * theta[3]]

t = np.arange(0,25,0.05)
sol0 = sp.odeint(dtheta1,thetazero,t)
plt.plot(sol0[:,0],sol0[:,2])
plt.xlabel(r'$\theta_1$')
plt.ylabel(r'$\theta_2$')
plt.show()