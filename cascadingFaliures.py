import scipy as sp
import numpy as np 
import systemGenerators as SG
import matrixModel as MM
import networkx as nx

gamma = 1
kappa = 1
P = []
def steadyState(thetas):
    delthetas = thetas[-1,1::2]
    for i in range (len(delthetas)):
        if(np.abs(delthetas[i]) < 0.01):
            return True
    return False

def checkDesync(thetas):
    for i in range(len(thetas)):
        if(np.abs(thetas[i]) > 1):
            return True
    return False

def edgePower(edge,thetas,kappa):
    thetas = thetas[-1,0::2]
    return kappa * np.sin(thetas[edge[1]] - thetas[edge[2]])

def dtheta(t,theta,G):
        A = nx.to_numpy_array(G)
        n = G.number_of_nodes()
        systems = []
        for i in range(n):
            systems.append(theta[2 * i + 1])
            system = P[i] - gamma * theta[2 * i + 1]
            for j in range(n):
                system -= kappa * A[i,j] * np.sin(theta[2 * i] - theta[2 * j])
            systems.append(system)
        return systems
def k1(f,t,y,h,G):
    return f(t,y,G)
def k2(f,t,y,h,G):
    return f(t + h/2, y + h/2 * k1(f,t,y,h),G)
def k3(f,t,y,h,G):
    return f(t + h/2, y + h/2 * k2(f,t,y,h),G)
def k4(f,t,y,h,G):
    return f(t + h/2, y + h * k3(f,t,y,h),G)
def timestep(G,thetazero):
    stepsize = 1/100
    thetas = thetazero + stepsize/6 * (k1(dtheta,0,thetazero,stepsize,G) + 2 * k2(dtheta,0,thetazero,stepsize,G) + 2 * k3(dtheta,0,thetazero,stepsize,G) + k4(dtheta,0,thetazero,stepsize,G))
    return thetas

def netMon(G,thetazero,alpha):
    S = 0
    finished = False
    while (finished == False):
        thetas = timestep(G,thetazero)
        if(checkDesync(thetas)):
            return 0
        if(steadyState(thetas)):
            return G.number_of_edges()
        for edge in list(G.edges):
            if(edgePower(edge,thetas) > alpha):
                finished = True
    for edge in list(G.edges):
        if(edgePower(edge,thetas) > alpha):
                G.remove_edge(edge)
    for i in range(G.number_of_nodes()):
        thetahzero = thetas[i]
        S += netMon(G,thetahzero,alpha)
    return S

def dynamicCascade(n,alpha):
    S = 0
    (sol,gen,con,pas,A,P,G) = MM.modelSystem(n)
    thetazero = sol
    n = G.number_of_nodes()
    m = G.number_of_edges()
    edges = list(G.edges)
    G.remove_edge(edges[0][0],edges[0][1])
    for i in range(n):
        thetahzero = thetazero[i : i + 1]
        S += netMon(G,thetahzero,alpha)
    return S/m

n=10
alpha = 1
kappa = n
print(dynamicCascade(n,alpha))