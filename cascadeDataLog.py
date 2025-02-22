import numpy as np 
import matrixModel as MM
import networkx as nx
import matplotlib.pyplot as plt
import systemGenerators as SG

gamma = 1
kappa = 1

def steadyState(thetas,lastthetas):
    for i in range (len(thetas)):
        if(np.abs(thetas[i] - lastthetas[i]) > 0.01):
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

def k1(f,t,y,h,G,P):
    return f(t,y,G,P)
def k2(f,t,y,h,G,P):
    return f(t + h/2, y + h/2 * k1(f,t,y,h,G,P),G,P)
def k3(f,t,y,h,G,P):
    return f(t + h/2, y + h/2 * k2(f,t,y,h,G,P),G,P)
def k4(f,t,y,h,G,P):
    return f(t + h/2, y + h * k3(f,t,y,h,G,P),G,P)
def timestep(G,thetazero,P):
    stepsize = 1/100
    thetas = thetazero + stepsize/6 * (k1(dtheta,0,thetazero,stepsize,G,P) + 2 * k2(dtheta,0,thetazero,stepsize,G,P) + 2 * k3(dtheta,0,thetazero,stepsize,G,P) + k4(dtheta,0,thetazero,stepsize,G,P))
    return thetas

def netMon(G,thetazero,alpha,P):
    S = 0
    finished = False
    n = G.number_of_nodes()
    lastthetazero = np.zeros(2 * n)
    sup = 0
    dem = 0
    for i in range(len(P)):
        if(P[i] < 0):
            dem += P[i]
        if(P[i] > 0):
            sup += P[i]
    for i in range(len(P)):
        if(P[i] < 0):
            P[i] = n * 1/dem
        if(P[i] > 0):
            P[i] = n * 1/sup
    while (finished == False):
        lastthetazero = thetazero
        thetazero = timestep(G,thetazero,P)
        if(checkAllDesync(thetazero)):
            finished = True
            break
        if(steadyState(thetazero,lastthetazero)):
            return G.number_of_edges()
        edges = list(G.edges)
        for i in range(len(edges)):
            if(edgePower(edges[i],thetazero,kappa,G) > alpha):
                finished = True
                break
    edges = list(G.edges)
    nodes = list(G.nodes)
    removed_edges = []
    removed_nodes = []
    for i in range(len(edges)):
        if(np.abs(edgePower(edges[i],thetazero,kappa,G)) > alpha):
            removed_edges.append((edges[i][0],edges[i][1]))
    for i in range(len(nodes)):
        if(checkSpecDesync(thetazero,i)):
            removed_nodes.append(nodes[i])
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
            if(Subgraph.number_of_nodes() > 0 and Subgraph.number_of_edges() > 0):
                pSub = []
                thetazeroSub =[]
                nodes = list(H.nodes)
                for i in c:
                    j = nodes.index(i)
                    pSub.append(P[j])
                    thetazeroSub.append(thetazeronew[2 * j])
                    thetazeroSub.append(thetazeronew[2 * j + 1])
                S += netMon(Subgraph,thetazeroSub,alpha,pSub)
            else:
                return 0
    else:
        return 0
    return S

def dynamicCascade(n,alpha,G,gen,con,pas,p):
    S = 0
    (sol,gen,con,pas,A,P,G) = MM.modelSystemFromSystem(n,gen,con,pas,p,G,False,gamma,kappa,40)
    thetazero = sol[-1,:]
    n = G.number_of_nodes()
    m = G.number_of_edges()
    edges = list(G.edges)
    bigEdge = 0
    bigEdgePower = 0
    for i in range(len(edges)):
        if(edgePower(edges[i],thetazero,kappa,G) > bigEdgePower):
            bigEdge = i
            bigEdgePower = edgePower(edges[i],thetazero,kappa,G)
    alpha = acastar * bigEdgePower
    G.remove_edge(edges[bigEdge][0],edges[bigEdge][1])
    S += netMon(G,thetazero,alpha,P)
    return S/(m-1)

n=20
alpha = 10
kappa = n
gamma = 1
gen = 10
con = 10
pas = 0
k = 4
p = 0.1
intervals = 100
G = nx.watts_strogatz_graph(n, k, p) 
print(G)
S = []
acastars = np.linspace(0.1,1,intervals)
for a in range(intervals):
    acastar = acastars[a]
    P = SG.randomisePower(gen,con,n)
    S.append(dynamicCascade(n,alpha,G.copy(),gen,con,pas,P))
    print("Completed "+ str(a + 1) + "/" + str(intervals) + ": S=" + str(S[-1]))
plt.plot(acastars,S)
plt.show()