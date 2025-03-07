import networkx as nx
import numpy as np
import systemGenerators as SG
import matrixModel as MM

G = nx.Graph()
G.add_nodes_from([0,1,2,3,4,5])
G.add_edges_from([(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)])
n = 6
gen = 3
con = 3
P = SG.randomisePower(gen,con,n)
print(P)
MM.modelSystemFromSystem(n,gen,con,0,P,G,True,1,n,10)
SG.drawNetwork(G,P)