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


def run_simulation(n,k,p,tmax,gen,con,pas):
    for i in range(100):
        kappa = (1.01 - i/100) * n
        print("trying kappa = " + str(kappa))
        P = SG.randomisePower(gen,con,n)
        (sols,A,P) = MM.modelSystemP(n,P,False,k,p,1,kappa,tmax)
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
            run_simulation(20,4,0.1,40,i,j,20 - i - j)
            print('completed: ' + str(i) + " generators and " + str(j) + " consumers.")
    wb.save("sample"+str(a)+".xlsx")
    print('done' + str(a))

