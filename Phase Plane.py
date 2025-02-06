import scipy.integrate as sp
import numpy as np
import matplotlib.pyplot as plt

A = np.matrix([[0,1],[1,0]])
P = [1,-1]#one producer one consumer
n = 2
gamma = 1
P_k = 0.2
kappa = 1/P_k
thetazero = [0,0]

def dw(w , t):
    return [w[1],
            2 - gamma * w[1] - 2 * kappa * np.sin(w[0])]

x = np.linspace(-np.pi,np.pi,1000)
y = np.linspace(-np.pi,np.pi,1000)
X, Y = np.meshgrid(x, y)
Xdot = Y
Ydot =  2 - gamma * Y - 2 * kappa * np.sin(X)
plt.streamplot(X,Y,Xdot,Ydot)
plt.xlabel(r'$\Delta\theta$')
plt.ylabel(r'$w$')
plt.legend()
plt.show()