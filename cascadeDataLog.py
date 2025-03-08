import numpy as np 
import matrixModel as MM
import networkx as nx
import matplotlib.pyplot as plt
import systemGenerators as SG
import cascadingFaliures as CF
import cascadePlus as CP
from openpyxl import Workbook

n=30
kappa = n
gamma = 1
gen = 15
con = 15
pas = 0
k = 4
p = 0.1
intervals = 10
wb = Workbook()
ws = wb.active
for i in range(10):
    G = nx.watts_strogatz_graph(n, k, p) 
    P = SG.randomisePower(gen,con,n)
    print(G.copy())
    print(P.copy())
    S = []
    acastars = np.linspace(0.5,1.5,intervals)
    for a in range(intervals):
        acastar = acastars[a]
        #S.append(CF.dynamicCascade(acastar,G.copy(),P.copy()))
        S.append(CP.dynamicCascade(acastar,G.copy(),P.copy()))
    ws.append(S)
wb.save("renamefile.xlsx")
#plt.plot(acastars,S)
#plt.show()