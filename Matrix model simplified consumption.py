import scipy.integrate as sp
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def generateSystem(n = 2):
    randint = np.random.random_integers(0,10,3)
    total = randint[0]+ randint[1] + randint[2]
    gen = 1
    con = 1
    n -= 2
    gen += (int)(n * randint[0]/total)
    con += (int)(n * randint[1]/total)
    pas = (int)(n * randint[2]/total)
    n += 2
    while(gen + con + pas < n):
        gen2 = (n * randint[0]/total) - gen
        con2 = (n * randint[1]/total) - con
        pas2 = (n * randint[2]/total) - pas
        max = np.max([gen2,con2,pas2])
        if(max == gen2):
            gen += 1
        elif(max == con2):
            con += 1
        elif(max == pas2):
            pas += 1
    print((gen,con,pas))
    return(gen,con,pas)
def dtheta(theta , t):
    systems = []
    for i in range(n):
        systems.append(theta[2 * i + 1])
        system = P[i] - gamma * theta[2 * i + 1]
        for j in range(n):
            system -= kappa * A[i,j] * np.sin(theta[2 * i] - theta[2 * j])
        systems.append(system)
    return systems

n = 10  # Number of nodes
k = 4  # Each node connects to k nearest neighbors
p = 0.1 # Rewiring probability

G = nx.watts_strogatz_graph(n, k, p) # Generate the Watts-Strogatz small-world network

A = nx.to_numpy_array(G) # Compute adjacency matrix
print(A)
Pmax = n
gamma = 1
thetazero = np.zeros(2 * n)
#thetazero[0] = 1
(gen,con,pas) = generateSystem(n)
P = np.zeros(n)
for i in range(n):
    if (i < gen):
        P[i] = Pmax/gen
    elif (i < gen + con):
        P[i] = -(Pmax)/con

t = np.arange(0,40,0.1)
plt.xlabel('t')
plt.ylabel(r'$\theta$')
for i in range(20):
    P_k = 0.3 + i * 0.3/20
    kappa = 1/P_k
    sol = sp.odeint(dtheta,thetazero,t)
    lines = plt.plot(t,sol[:,0::2],label = P_k)
    plt.legend()
    plt.draw()
    #plt.show()
    if(np.abs(sol[-1,0] - sol[-2,0])>0.01):
        print('Failure')
        print(P_k)
    plt.pause(1)
    for line in lines:
        line.remove()
