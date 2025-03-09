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
acastars = np.linspace(0.5,1.5,intervals)
ws.append(list(acastars))
for i in range(10):
    G = nx.watts_strogatz_graph(n, k, p) 
    P = SG.randomisePower(gen,con,n)
    Data1 = []
    Data2 = []
    Data3 = []
    Data4 = []
    for a in range(intervals):
        acastar = acastars[a]
        #S.append(CF.dynamicCascade(acastar,G.copy(),P.copy()))
        (S,edgesBroken,nodesFailed,cascadeTime) = CP.dynamicCascade(acastar,G.copy(),P.copy(),False)
        print(S,edgesBroken,nodesFailed,cascadeTime)
        Data1.append(S)
        Data2.append(edgesBroken)
        Data3.append(nodesFailed)
        Data4.append(edgesBroken)
    ws.append(Data1)
    ws.append(Data2)
    ws.append(Data3)
    ws.append(Data4)
wb.save("renamefile.xlsx")
#plt.plot(acastars,S)
#plt.show()