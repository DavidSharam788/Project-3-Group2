import numpy as np 
import matrixModel as MM
import networkx as nx
import matplotlib.pyplot as plt
import systemGenerators as SG
import cascadingFaliures as CF

n=10
kappa = n
gamma = 1
gen = 5
con = 5
pas = 0
k = 4
p = 0.1
G = nx.watts_strogatz_graph(n, k, p) 
P = SG.randomisePower(gen,con,n)
S = 0
stepsize = 1
tol = 0.1
acastar = 1.3
Slast = 0
while np.abs(S-0.5) > tol:
    S = CF.dynamicCascade(acastar,G.copy(),P.copy())
    print(S)
    print(acastar)
    if((Slast > 0.5 and S < 0.5) or (Slast < 0.5 and S > 0.5)):
        stepsize = stepsize/2
    if(S-0.5 > 0):
        acastar -=  tol * stepsize
    elif(S-0.5 < 0):
        acastar +=  tol * stepsize
    Slast = S