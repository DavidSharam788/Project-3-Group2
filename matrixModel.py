import scipy.integrate as sp
import numpy as np
import matplotlib.pyplot as plt
import systemGenerators as SG
import networkx as nx

def modelSystem(n,drawGraph = True,k = 4,p = 0.1,gamma = 1, kappa = 5,tmax = 40):
    thetazero = np.zeros(2 * n)
    (gen,con,pas,A,P,G) = SG.generateRandomWSSsystem(n,k,p)
    def dtheta(theta , t):
        systems = []
        for i in range(n):
            systems.append(theta[2 * i + 1])
            system = P[i] - gamma * theta[2 * i + 1]
            for j in range(n):
                system -= kappa * A[i,j] * np.sin(theta[2 * i] - theta[2 * j])
            systems.append(system)
        return systems
    t = np.linspace(0,tmax,100)
    sol = sp.odeint(dtheta,thetazero,t)
    if(drawGraph):
        plt.plot(t,sol[:,0::2])
        plt.xlabel('t')
        plt.ylabel(r'$\theta$')
        plt.show()
    return (sol,gen,con,pas,A,P,G)

def modelSystemP(n,P,drawGraph = True,k = 4,p = 0.1,gamma = 1, kappa = 5,tmax = 40):
    thetazero = np.zeros(2 * n)
    A = SG.generateRandomWSSsystemP(n,k,p)
    def dtheta(theta , t):
        systems = []
        for i in range(n):
            systems.append(theta[2 * i + 1])
            system = P[i] - gamma * theta[2 * i + 1]
            for j in range(n):
                system -= kappa * A[i,j] * np.sin(theta[2 * i] - theta[2 * j])
            systems.append(system)
        return systems
    t = np.linspace(0,tmax,100)
    sol = sp.odeint(dtheta,thetazero,t)
    if(drawGraph):
        plt.plot(t,sol[:,0::2])
        plt.xlabel('t')
        plt.ylabel(r'$\theta$')
        plt.show()
    return (sol,A,P)

def modelSystemFromSystem(n,gen,con,pas,P,G,drawGraph = True ,gamma = 1, kappa = 5,tmax = 40):
    thetazero = np.zeros(2 * n)
    A = nx.to_numpy_array(G)
    def dtheta(theta , t):
        systems = []
        for i in range(n):
            systems.append(theta[2 * i + 1])
            system = P[i] - gamma * theta[2 * i + 1]
            for j in range(n):
                system -= kappa * A[i,j] * np.sin(theta[2 * i] - theta[2 * j])
            systems.append(system)
        return systems
    t = np.linspace(0,tmax,100)
    sol = sp.odeint(dtheta,thetazero,t)
    if(drawGraph):
        plt.plot(t,sol[:,0::2])
        plt.xlabel('t')
        plt.ylabel(r'$\theta$')
        plt.show()
    return (sol,gen,con,pas,A,P,G)

#(sol,gen,con,pas,A,P) = modelSystem(6,True,2,0.1,1,10,20)

#print(sol[-1,1::2])