import numpy as np
import networkx as nx

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
        else:
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


#print(generateRandomWSSsystem(4))