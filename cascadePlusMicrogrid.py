import numpy as np 
import MicrogridsWithBatteries as MGB
import Microgrids as MG
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
    thetas = NM.RungeKutta4(G,thetazero,P,stepsize,dtheta)
    #thetas = NM.RKF(G,thetazero,P,stepsize,dtheta)
    return (thetas,stepsize)

def netMon(G,thetazero,alpha,Solars,debug = False):
    if(G.number_of_edges() == 0):
        return (0,0,0,0)
    S = 0
    edgesBroken = 0
    nodesFailed = 0
    cascadeTime = 0
    finished = False
    n = G.number_of_nodes()
    lastthetazero = np.zeros(2 * n)
    while (finished == False):
        lastthetazero = thetazero
        P = np.zeros(n)
        total = 0
        for i in range(1,n):
            P[i] = MG.netPower(cascadeTime,i,Solars)
            total += P[i]
        P[0] = -1 * total
        (thetazero,time) = timestep(G,thetazero,P)
        cascadeTime += time
        if(checkAllDesync(thetazero)):
            if(debug):
                print("Desync")
            finished = True
            break
        if(steadyState(thetazero,lastthetazero)):
            if(debug):
                print("Steady state")
            return (G.number_of_edges(),edgesBroken,nodesFailed,cascadeTime)
        edges = list(G.edges)
        for i in range(len(edges)):
            if(edgePower(edges[i],thetazero,kappa,G) > alpha):
                if(debug):
                    print("Edge Overload: " + str(edgePower(edges[i],thetazero,kappa,G)))
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
    edgesBroken += len(removed_edges)
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
    nodesFailed += G.number_of_edges() - H.number_of_edges() - edgesBroken
    maxTime = 0
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
            (D,edgesBrokenNew,nodesFailedNew,time) = netMon(Subgraph,thetazeroSub,alpha,pSub,debug)
            S+=D
            edgesBroken += edgesBrokenNew
            nodesFailed += nodesFailedNew
            if(time > maxTime):
                maxTime = time
        cascadeTime+= maxTime
    else:
        return (0,edgesBroken,nodesFailed,cascadeTime)
    return (S,edgesBroken,nodesFailed,cascadeTime)

def dynamicCascade(alphastar,G,Solars,debug = False):
    S = 0
    n = len(Solars)
    sol = MG.modelSystemFromSystem(n,Solars,G,False,gamma,n,24)
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
    (S,edgesBroken,nodesFailed,cascadeTime) = netMon(G,thetazero,alpha,Solars,debug)
    return (S/(m-1),edgesBroken,nodesFailed,cascadeTime)
n = 10
alphastar = 30
Solars = SG.randomSolars(n,4)
G = nx.watts_strogatz_graph(n, 4, 0.1) 
#print(dynamicCascade(alphastar,G,Solars,True))
