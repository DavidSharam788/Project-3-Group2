import scipy.integrate as sp
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from openpyxl import Workbook
import matrixModel as MM
import systemGenerators as SG
import datetime

def checkDesync(sols,n):
    thetasols = sols[:,0::2]
    for i in range(n):
        if(np.abs(thetasols[-1,i]) > 1):
            return True
    return False


def run_simulation(n,tmax,gen,con,pas):
    for i in range(100):
        kappa = (1.01 - i/100) * n
        print("trying kappa = " + str(kappa))
        P = SG.randomisePower(gen,con,n)
        G = SG.barabasi_albert_graph(n,2)
        (sols,gen,con,pas,A,P,G) = MM.modelSystemFromSystem(n,gen,con,pas,P,G,False,1,kappa,tmax)
        if(checkDesync(sols,n)):
            ws.append([gen,con,pas,kappa/n])
            break
        elif(i == 99):
            ws.append([gen,con,pas,0])

for a in range(10):
    wb = Workbook()
    ws = wb.active
    for i in range(0,21): #gen
        for j in range(0,21 - i): #con
            run_simulation(20,40,i,j,20 - i - j)
            print('completed: ' + str(i) + " generators and " + str(j) + " consumers.")
    wb.save("sampleBA"+str(a)+".xlsx")
    print('done' + str(a))

