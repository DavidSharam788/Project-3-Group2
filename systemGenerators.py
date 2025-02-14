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
    return(gen,con,pas)
def randomisePower(gen,con,n):
    P = np.zeros(n)
    for i in range(n):
        if (i < gen):
            P[i] = n/gen
        elif (i < gen + con):
            P[i] = -n/con
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
    return(gen,con,pas,A,P)

def generateRandomWSSsystemP(n,k = 2,p = 0.1):
    G = nx.watts_strogatz_graph(n, k, p) 
    A = nx.to_numpy_array(G)
    return(A)



#print(generateRandomWSSsystem(4))