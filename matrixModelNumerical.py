import scipy.integrate as sp
import numpy as np
import matplotlib.pyplot as plt
import systemGenerators as SG
import networkx as nx
from matplotlib.patches import Arc

def nextSquare(n):
    guess = 0
    while (guess**2 < n):
        guess += 1
    return guess
def DrawGraph(sol,t):
    sol = sol[:,0::2]
    n = len(sol[0,:])
    dim = nextSquare(n)
    fig, axs = plt.subplots(dim, dim)
    fig.suptitle('Rotating machines')
    for ax in fig.get_axes():
            ax.label_outer()
    for a in range(100):
        thetaBase = 2 * np.pi/50 * t[a]
        circles = []
        arcs = []
        scattersb = []
        scattersr = []
        done = 0
        for i in range(dim):
            for j in range(dim):
                if(done < n):
                    circle = plt.Circle((0, 0), 1, color='b', fill=False)
                    circles.append(circle)
                    arc = Arc((0, 0), 2, 2, color='y', theta1=np.degrees(thetaBase - 1), theta2=np.degrees(thetaBase + 1))
                    arcs.append(arc)
                    axs[i,j].add_patch(circle)
                    axs[i,j].add_patch(arc)
                    axs[i,j].set_xlim(-1.1,1.1)
                    axs[i,j].set_ylim(-1.1,1.1)
                    scatterb = axs[i,j].scatter(np.cos(thetaBase + sol[a,done]), np.sin(thetaBase + sol[a,done]), c= 'b',label = r'$\theta = $' + str(np.round(sol[a,done],3)))
                    scatterr = axs[i,j].scatter(np.cos(thetaBase), np.sin(thetaBase), c = 'r')
                    axs[i,j].legend()
                    scattersb.append(scatterb)
                    scattersr.append(scatterr)
                elif(done == n):
                    axs[i,j].plot(t,sol[:,0::2])
                    axs[i,j].set_xlim(0,10)
                    axs[i,j].set_ylim(-0.1,0.1)
                done += 1
                
        plt.draw()
        plt.pause(0.01)
        for i in range(n):
            circles[i].remove()
            arcs[i].remove()
            scattersb[i].remove()
            scattersr[i].remove()
        
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
        DrawGraph(sol,t)
    return (sol,gen,con,pas,A,P,G)

n=15
kappa = n
gamma = 1
gen = 7
con = 8
pas = 0
k = 4
p = 0.1
G = nx.watts_strogatz_graph(n, k, p) 
P = SG.fixedAlternatePower(gen,con,n)
modelSystemFromSystem(15,gen,con,pas,P,G,True,gamma,kappa,20)

#print(sol[-1,1::2])