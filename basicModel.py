import scipy.integrate as sp
import numpy as np
import matplotlib.pyplot as plt

A = np.matrix([[0,1],[1,0]])
P = [1,-1]#one producer one consumer
n = 2
gamma = 1
P_k = 1
kappa = 1/P_k
thetazero = [0,0,0,0]
deltatheta = 1

def dtheta(theta , t):
    return [theta[1], #theta1
            P[0] - kappa * np.sin(theta[0] - theta[2]) - gamma * theta[1], #dtheta1
            theta[3], #theta2
            P[1] - kappa * np.sin(theta[2] - theta[0]) - gamma * theta[3]] #dtheta2

t = np.arange(0,25,0.05)
sol0 = sp.odeint(dtheta,thetazero,t)
print(np.shape(sol0))
print(sol0[:,0])
plt.plot(t,sol0[:,0],label = r'$\theta_1$')
plt.plot(t,sol0[:,2],label = r'$\theta_2$')
plt.plot(t,kappa * np.sin(sol0[:,0] - sol0[:,2]),label = r'$f_{12}$')
plt.xlabel('t')
plt.ylabel(r'$\theta$')
plt.legend()
plt.show()