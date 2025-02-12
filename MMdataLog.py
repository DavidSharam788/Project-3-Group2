import scipy.integrate as sp
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from openpyxl import Workbook
import matrixModel as MM


def run_simulation(n,k,p,tmax):
    for i in range(100):
        kappa = (1.01 - i/100) * n
        (sols,gen,con,pas,A,P) = MM.modelSystem(n,False,k,p,1,kappa,tmax)
        if(np.abs(sols[-1,0] - sols[-2,0]) > 0.01):
            ws.append([gen,con,pas,kappa/n])
        elif(i == 99):
            ws.append([gen,con,pas,0])

wb = Workbook()
ws = wb.active
for i in range(200):
    run_simulation(10,4,0.1,40)
    print('completed ' + str(i))
wb.save("sample.xlsx")
print('done')

