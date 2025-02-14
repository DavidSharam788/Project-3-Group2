import scipy as sp
import numpy as np 
import systemGenerators as SG
import matrixModel as MM
import networkx as nx


def edgePower(G,edge,theta,kappa):
    return kappa * np.sin(theta[edge[1] - edge[2]])

def timestep():
    return 0

def netMon(G,theta,alpha,kappa):
    S = 0
    finished = False
    while (finished == False):
        thetas = timestep()
        if(np.abs(theta) > alpha):
            return 0
        if(np.abs(thetas[-1,0] - thetas[-2,0]) > 0.01):
            return G.number_of_edges()
    for edge in G.edges():
        if(edgePower(G,edge,theta,kappa) > alpha):
                G.remove_edge(edge)
    for i in range(G.nodes):
        thetah = theta[i]
        S += netMon(G,thetah,alpha)
    return S

def dynamicCascade(n,alpha):
    S = 0
    (sol,gen,con,pas,A,P,G) = MM.modelSystem(n)
    theta = sol[-1,0::2]
    n = G.number_of_nodes()
    m = G.number_of_edges()
    edges = G.edges()
    G.remove_edge(edges[1])
    for i in range(G.nodes):
        thetah = theta[i]
        S += netMon(G,thetah,alpha)
    return S/m

n=10

print(dynamicCascade(n))