import numpy as np 
import matrixModel as MM
import networkx as nx
import matplotlib.pyplot as plt
import systemGenerators as SG
import cascadingFaliures as CF

n=16
kappa = n
gamma = 1
gen = 8
con = 8
pas = 0
k = 4
p = 0.1
G = nx.watts_strogatz_graph(n, k, p) 
P = SG.randomisePower(gen,con,n)
S = 0
stepsize = 0.5
tol = 0.01
A = 1
Slast = 0
Alast = 0
while np.abs(Alast-A) > tol:
    S = CF.dynamicCascade(A,G.copy(),P.copy())
    #print(np.abs(Alast-A))
    print(A)
    if((Slast > 0.5 and S < 0.5) or (Slast < 0.5 and S > 0.5)):
        stepsize = stepsize/2
    Slast = S
    Alast = A
    if(S-0.5 > 0):
        A -= stepsize
    elif(S-0.5 < 0):
        A += stepsize
print('done')
print(S)

