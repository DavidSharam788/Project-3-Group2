import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


G = nx.random_lobster(10,0.2,0.2)
nx.draw(G)
plt.show()