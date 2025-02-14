import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


G = nx.random_lobster(20,0.5,0.1)
nx.draw(G)
plt.show()