import scipy as sp
import numpy as np 
import systemGenerators as SG
import matrixModel as MM

def netMon(G,theta,alpha):
    S = 0
    for power in P:
        power = n/gen * power/np.mod(power)
    finished = False
    while (finished == False):
        timestep()
        if(frequency() > tol):
            return 0
        if(steadystate):
            return countEdges()
        for edges in G:
            if(edgeFlow() > alpha):
                finished = True
    deleteOverloadedEdges()
    for H in G:
        thetah = theta[H]
        S += netMon(H,thetah , alpha)
    return S

def dynamicCascade(n,alpha):
    S = 0
    (sol,gen,con,pas,A,P) = MM.modelSystem(n)
    theta =
    m =
    removeEdge()
    for H in A:
        thetah = theta[H]
        S += netMon(A,thetah,alpha)
    return S/m

n=10

print(dynamicCascade(n))