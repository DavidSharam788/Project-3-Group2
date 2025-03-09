import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

def barabasi_albert_graph(n, m, seed=None):
    if m < 1 or m >= n:
        raise nx.NetworkXError(
            "Barabási–Albert network must have m >= 1 and m < n, "
            "m = %d, n = %d" % (m, n)
        )
    if seed is not None:
        random.seed(seed)
    G = nx.empty_graph(m)
    G.name = "barabasi_albert_graph(%s,%s)" % (n, m)
    targets = list(range(m))
    repeated_nodes = []
    source = m
    while source < n:
        G.add_edges_from(zip([source] * m, targets))
        repeated_nodes.extend(targets)
        repeated_nodes.extend([source] * m)
        targets = random.sample(repeated_nodes, m)
        source += 1

    return G

def randomiseNodeTypes(n):
    randint = np.random.random_integers(0,10,3)
    total = randint[0]+ randint[1] + randint[2]
    gen = (int)(n * randint[0]/total)
    con = (int)(n * randint[1]/total)
    pas = (int)(n * randint[2]/total)
    while(gen + con + pas < n):
        gen2 = (n * randint[0]/total) - gen
        con2 = (n * randint[1]/total) - con
        pas2 = (n * randint[2]/total) - pas
        max = np.max([gen2,con2,pas2])
        if(max == gen2):
            gen += 1
        elif(max == con2):
            con += 1
        elif(max == pas2):
            pas += 1
    return(gen,con,pas)#

def fixedAlternatePower(gen,con,n):
    P = np.zeros(n)
    matched = 0
    if(gen < con):
        matched = gen
    else:
        matched = con
    for i in range(matched):
        P[2 * i] =  n/gen
        P[2 * i + 1] = -n/con
    for i in range(matched,n-matched):
        if(gen > i):
            P[2 * i] =  n/gen
        elif(con > i):
            P[2 * i] = -n/con
        else:
            P[2 * i] = 0
    return P


def randomisePower(gen,con,n):
    currentGen = 0
    currentCon = 0
    P = np.zeros(n)
    for i in range(n):
        if(currentCon < con):
            if(currentGen < gen):
                if(np.random.random() > 0.5):
                    P[i] = n/gen
                    currentGen += 1
                else:
                    P[i] = -n/con
                    currentCon += 1
            else:
                P[i] = -n/con
                currentCon += 1
        elif(currentGen < gen):
            P[i] = n/gen
            currentGen += 1
    return P
def generateRandomSystem(n):
    (gen,con,pas) = randomiseNodeTypes(n)
    A = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if(i != j):
                A[i,j] = np.random.random_integers(0,100)/100  
    P = randomisePower(gen,con,n)
    return(gen,con,pas,A,P)

def generateRandomWSSsystem(n,k = 2,p = 0.1):
    (gen,con,pas) = randomiseNodeTypes(n)
    G = nx.watts_strogatz_graph(n, k, p) 
    A = nx.to_numpy_array(G)
    P = randomisePower(gen,con,n)
    return(gen,con,pas,A,P,G)

def generateRandomWSSsystemP(n,k = 2,p = 0.1):
    G = nx.watts_strogatz_graph(n, k, p) 
    A = nx.to_numpy_array(G)
    return(A)

def drawNetwork(G,P):
    gen = []
    con = []
    pas = []
    nodes = list(G.nodes)
    for i in range(len(P)):
        if(P[i] > 0):
            gen.append(nodes[i])
        elif(P[i] < 0):
            con.append(nodes[i])
        else:
            pas.append(nodes[i])
        
    pos = nx.circular_layout(G,1)
    options = {"edgecolors": "black", "node_size": 800, "alpha": 1}
    if(len(gen)>0):
        nx.draw_networkx_nodes(G, pos, nodelist=gen, node_color="tab:red", **options)
    if(len(con)>0):
        nx.draw_networkx_nodes(G, pos, nodelist=con, node_color="tab:blue", **options)
    if(len(pas)>0):
        nx.draw_networkx_nodes(G, pos, nodelist=pas, node_color="tab:gray", **options)
    nx.draw_networkx_edges(G, pos,width = 2)
    nx.draw_networkx_labels(G, pos,font_weight='bold')
    plt.show()

def randomSolars(n,s):
    Solars = np.zeros(n)
    for i in range(s):
        found = False
        while found == False:
            if(Solars[random.randint(1,n-1)] == 0):
                Solars[random.randint(1,n-1)] = 1
                found = True
    return Solars
#print(generateRandomWSSsystem(4))
# G = barabasi_albert_graph(20, 2)
# P = randomisePower(10,10,20)
# drawNetwork(G,P)