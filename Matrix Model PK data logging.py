import scipy.integrate as sp
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from openpyxl import Workbook

gamma = 1

def generateSystem(n):
    randint = np.random.random_integers(1,10,3)
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
def dtheta(theta , t):
    n = len(P)
    systems = []
    for i in range(n):
        systems.append(theta[2 * i + 1])
        system = P[i] - gamma * theta[2 * i + 1]
        for j in range(n):
            system -= kappa * A[i,j] * np.sin(theta[2 * i] - theta[2 * j])
        systems.append(system)
    return systems

def run_simulation(n = 10,k = 4,p = 0.1,tmax = 40):
    global A,P,kappa
    G = nx.watts_strogatz_graph(n, k, p) 
    A = nx.to_numpy_array(G)
    thetazero = np.zeros(2 * n)
    (gen,con,pas) = generateSystem(n)
    P = np.zeros(n)
    for i in range(n):
        if (i < gen):
            P[i] = n/gen
        elif (i < gen + con):
            P[i] = -(n)/con
    t = np.arange(0,tmax,0.1)
    plt.xlabel('t')
    plt.ylabel(r'$\theta$')
    for i in range(100):
        kappa = (1.01 - i/100)* n
        sol = sp.odeint(dtheta,thetazero,t)
        if(np.abs(sol[-1,0] - sol[-2,0])>0.01):
            ws.append([gen, con, pas,kappa/n])
            print(kappa/n)
            break
        elif(i == 99):
            ws.append([gen, con, pas,0])
wb = Workbook()
ws = wb.active
for i in range(200):
    run_simulation(10,4,0.1,40)
    print('completed ' + str(i))
wb.save("sample.xlsx")
print('done')

