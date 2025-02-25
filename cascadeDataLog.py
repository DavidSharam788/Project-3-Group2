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
intervals = 10
G = nx.watts_strogatz_graph(n, k, p) 
P = SG.randomisePower(gen,con,n)
print(G.copy())
print(P.copy())
S = []
acastars = np.linspace(0.5,1,intervals)
for a in range(intervals):
    acastar = acastars[a]
    S.append(CF.dynamicCascade(acastar,G.copy(),P.copy()))
    print("Completed "+ str(a + 1) + "/" + str(intervals) + ": S=" + str(S[-1]))
plt.plot(acastars,S)
plt.show()