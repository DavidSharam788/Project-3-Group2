import numpy as np 
import matrixModel as MM
import networkx as nx
import matplotlib.pyplot as plt
import systemGenerators as SG
import NumericalMethods as NM

gamma = 1
kappa = 1

def steadyState(thetas,lastthetas):
    for i in range (len(thetas)):
        if(np.abs(thetas[i] - lastthetas[i]) > 0.0001):
            return False
    return True


def checkSpecDesync(thetas,i):
    thetas = thetas[1::2]
    if(np.abs(thetas[i]) > 1):
        return True
    return False

def checkAllDesync(thetas):
    thetas = thetas[1::2]
    for i in range(len(thetas)):
        if(np.abs(thetas[i]) > 1):
            return True
    return False

def edgePower(edge,thetas,kappa,G):
    thetas = thetas[0::2]
    nodes = list(G.nodes)
    leftIndex = 0
    rightIndex = 0
    for i in range(len(nodes)):
        if(nodes[i] == edge[0]):
            leftIndex = i
        if(nodes[i] == edge[1]):
            rightIndex = i
    return kappa * np.sin(thetas[leftIndex] - thetas[rightIndex])

def dtheta(t,theta,G,P):
    A = nx.to_numpy_array(G)
    n = G.number_of_nodes()
    systems = np.zeros(n * 2)
    for i in range(n):
        systems[2 * i] = theta[2 * i + 1]
        system = P[i] - gamma * theta[2 * i + 1]
        for j in range(n):
            system -= kappa * A[i,j] * np.sin(theta[2 * i] - theta[2 * j])
        systems[2 * i + 1] = system
    return systems

def timestep(G,thetazero,P):
    stepsize = 1/2000
    #thetas = NM.RungeKutta4(G,thetazero,P,stepsize,dtheta)
    thetas = NM.RKF(G,thetazero,P,stepsize,dtheta)
    return thetas

def netMon(G,thetazero,alpha,P,debug = False):
    S = 0
    finished = False
    n = G.number_of_nodes()
    lastthetazero = np.zeros(2 * n)
    sup = 0
    dem = 0
    for i in range(len(P)):
        if(P[i] < 0):
            dem += 1
        if(P[i] > 0):
            sup += 1
    if(debug):
        print(str(sup) + " " + str(dem) + " " + str(n))
    if(sup == 0 or dem == 0):
        if(debug):            
            print("Not enough gen/con to steady state")
        return 0
    for i in range(len(P)):
        if(P[i] < 0):
            P[i] = -n/dem
        if(P[i] > 0):
            P[i] = n/sup
    
    while (finished == False):
        lastthetazero = thetazero
        thetazero = timestep(G,thetazero,P)
        if(checkAllDesync(thetazero)):
            if(debug):
                print("Desync")
            finished = True
            break
        if(steadyState(thetazero,lastthetazero)):
            if(debug):
                print("Steady state")
                nx.draw(G)
                plt.show()
            return G.number_of_edges()
        edges = list(G.edges)
        for i in range(len(edges)):
            if(edgePower(edges[i],thetazero,kappa,G) > alpha):
                if(debug):
                    print("Edge Overload")
                finished = True
                break
    edges = list(G.edges)
    nodes = list(G.nodes)
    removed_edges = []
    removed_nodes = []
    for i in range(len(edges)):
        if(np.abs(edgePower(edges[i],thetazero,kappa,G)) > alpha):
            removed_edges.append((edges[i][0],edges[i][1]))
            if(debug):
                print("remove "+ str((edges[i][0],edges[i][1])))
    for i in range(len(nodes)):
        if(checkSpecDesync(thetazero,i)):
            removed_nodes.append(nodes[i])
            if(debug):
                print("remove "+ str(nodes[i]))
    thetazeronew = []
    Pnew = []
    H = nx.Graph()
    for i in range(len(nodes)):
        if (not nodes[i] in removed_nodes):
            H.add_node(nodes[i])
            thetazeronew.append(thetazero[2 * i])
            thetazeronew.append(thetazero[2 * i + 1])
            Pnew.append(P[i])
    for i in range(len(edges)):
        if(not edges[i] in removed_edges and not edges[i][0] in removed_nodes and not edges[i][1] in removed_nodes):
            H.add_edge(edges[i][0], edges[i][1])
    if(H.number_of_nodes() > 0 and H.number_of_edges() > 0):
        for c in nx.connected_components(H):
            Subgraph = H.subgraph(c).copy()
            if(debug):       
                print(Subgraph)
            pSub = []
            thetazeroSub =[]
            nodes = list(H.nodes)
            for i in c:
                j = nodes.index(i)
                pSub.append(P[j])
                thetazeroSub.append(thetazeronew[2 * j])
                thetazeroSub.append(thetazeronew[2 * j + 1])
            S += netMon(Subgraph,thetazeroSub,alpha,pSub,debug)
    else:
        return 0
    return S

def dynamicCascade(alphastar,G,p,debug = False):
    S = 0
    n = len(p)
    gen = 0
    con = 0
    pas = 0
    for i in range(n):
        if(p[i] > 0):
            gen += 1
        elif(p[i] < 0):
            con += 1
        else:
            pas += 1
    (sol,gen,con,pas,A,P,G) = MM.modelSystemFromSystem(n,gen,con,pas,p,G,False,gamma,kappa,40)
    if(debug):
        print(gen,con,pas)
        print(G)
    thetazero = sol[-1,:]
    n = G.number_of_nodes()
    m = G.number_of_edges()
    edges = list(G.edges)
    bigEdge = 0
    bigEdgePower = 0
    for i in range(len(edges)):
        if(np.abs(edgePower(edges[i],thetazero,kappa,G)) > bigEdgePower):
            bigEdge = i
            bigEdgePower = np.abs(edgePower(edges[i],thetazero,kappa,G))
    alpha = alphastar * bigEdgePower
    if(debug):
        print("alpha=" + str(alpha))
    G.remove_edge(edges[bigEdge][0],edges[bigEdge][1])
    S += netMon(G,thetazero,alpha,P,debug)
    return S/(m-1)

n=30
alpha = 10
alphastar = 0.5
kappa = n
gamma = 1
gen = 15
con = 15
pas = 0
k = 4
p = 0.1
G = nx.watts_strogatz_graph(n, k, p) 
P = SG.randomisePower(gen,con,n)
print(dynamicCascade(alphastar,G,P,True))
