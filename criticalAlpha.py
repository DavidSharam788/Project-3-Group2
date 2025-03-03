import numpy as np 
import matrixModel as MM
import networkx as nx
import matplotlib.pyplot as plt
import systemGenerators as SG
import cascadingFaliures as CF

n=30
kappa = n
gamma = 1
gen = 15
con = 15
pas = 0
k = 4
p = 0.1
G = nx.watts_strogatz_graph(n, k, p) 
P = SG.randomisePower(gen,con,n)
S = 0
stepsize = 0.5
tol = (n * 2 - 1)/2
tol2 = int((n * 2 - 1)/2)
tol3 = 0.5 - np.abs((tol2 - tol))
print(tol3)
acastar = 1
Slast = 0
while np.abs(S-0.5) > tol3:
    S = CF.dynamicCascade(acastar,G.copy(),P.copy())
    print(S)
    print(acastar)
    if((Slast > 0.5 and S < 0.5) or (Slast < 0.5 and S > 0.5)):
        stepsize = stepsize/2
    if(S-0.5 > 0):
        acastar -= stepsize
    elif(S-0.5 < 0):
        acastar += stepsize
    Slast = S