import numpy as np 
import matrixModel as MM
import networkx as nx
import matplotlib.pyplot as plt
import systemGenerators as SG
import cascadePlusMicrogrid as CPM
from openpyxl import Workbook

n=10
kappa = n
intervals = 10
wb = Workbook()
ws = wb.active
acastars = np.linspace(1,15,intervals)
ws.append(list(acastars))
for i in range(10):
    G = nx.watts_strogatz_graph(n, 4, 0.1) 
    Solars = SG.randomSolars(n,4)
    Data1 = []
    Data2 = []
    Data3 = []
    Data4 = []
    for a in range(intervals):
        acastar = acastars[a]
        #S.append(CF.dynamicCascade(acastar,G.copy(),P.copy()))
        (S,edgesBroken,nodesFailed,cascadeTime) = CPM.dynamicCascade(acastar,G.copy(),Solars.copy(),False)
        print(S,edgesBroken,nodesFailed,cascadeTime)
        Data1.append(S)
        Data2.append(edgesBroken)
        Data3.append(nodesFailed)
        Data4.append(cascadeTime)
    ws.append(Data1)
    ws.append(Data2)
    ws.append(Data3)
    ws.append(Data4)
wb.save("renamefile.xlsx")
#plt.plot(acastars,S)
#plt.show()