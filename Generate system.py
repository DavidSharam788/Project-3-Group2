import numpy as np
import matplotlib.pyplot as plt


def generateSystem(n = 2):
    randint = np.random.random_integers(0,10,3)
    total = randint[0]+ randint[1] + randint[2]
    gen = 1
    con = 1
    n -= 2
    gen += (int)(n * randint[0]/total)
    con += (int)(n * randint[1]/total)
    pas = (int)(n * randint[2]/total)
    n += 2
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
    print((gen,con,pas))
    return(gen,con,pas)

def connectSystem(gen,con,pas):
    n = gen + con + pas
    A = np.zeros((n,n))

    for i in range(n):
        for j in range(n):
            if(i != j):
                A[i,j] = np.random.random_integers(0,100)/100
    print(A)
    return A

n = 4
(gen,con,pas) = generateSystem(n)
A = connectSystem(gen,con,pas)
P = np.zeros(n)
for i in range(n):
    if (i < gen):
        P[i] = 1
    elif (i < gen + con):
        P[i] = -(1 * gen)/con
print(P)