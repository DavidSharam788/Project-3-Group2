import scipy.integrate as sp
import numpy as np
import matplotlib.pyplot as plt
import systemGenerators as SG
import networkx as nx
import math

batteryMaxStorage = 14
batteryMaxChargeRate = 5
batteryStored = 0

def poly_eval(func,t):
    n = len(func)
    val = 0
    for i in range(n):
        val += func[i] * t ** (n - i - 1)
    return val
def getGen(t):
    data = [0,0,0,0,0.622016344,21.74464872,95.51953841,217.3773838,456.7443442,725.4340889,830.5684928,947.7618554,983.3830465,990.9596477,893.1107507,703.8849027,460.4322079,199.7553666,63.20175334,13.01241297,0.179181048,0,0,0]
    func = np.polyfit(np.linspace(0,24*360,24),data,6)
    noise = np.random.normal(0,0.1)
    return  poly_eval(func,t)/1000 
def getCon(t):
    data = [0.13685621,0.129153595,0.117801627,0.109375184,0.104326979,0.10166637,0.098873444,0.09756139,0.098316364,0.102370853,0.107608668,0.119756377,0.134899031,0.152341197,0.164731619,0.172713593,0.175476122,0.178149543,0.179055014,0.178912604,0.17795443,0.177666743,0.179180521,0.182123092,0.1823951,0.180441194,0.176229569,0.172718478,0.170589968,0.171114662,0.174018072,0.181277699,0.189514855,0.200496971,0.209157038,0.220687479,0.227244904,0.230595116,0.230441816,0.234352963,0.238461013,0.242345634,0.240609095,0.233917157,0.213938825,0.189474045,0.165858775,0.145714687]
    func = np.polyfit(np.linspace(0,48*360,48),data,6)
    noise = np.random.normal(0,0.01)
    return poly_eval(func,t)
def netPower(t,i,Solars):
    power = -1 * getCon(t)
    if(Solars[i] == 1):
        power += getGen(t)
    return power

def doBattery(P):
    rate = 0
    if(P>0):
        if(P > 5):
            P = 5
        rate = 5
    elif(P < 0 and batteryStored > 0):
        rate = -5
    batteryStored += rate/60
    if(batteryStored > 14):
        batteryStored = 14
    return 0

def modelSystemFromSystem(n,Solars,G,drawGraph = True ,gamma = 1, kappa = 10,tmax = 24):
    thetazero = np.zeros(2 * n)
    A = nx.to_numpy_array(G)
    def dtheta(theta , t):
        systems = []
        P = np.zeros(n)
        total = 0
        for i in range(1,n):
            P[i] = netPower(t,i,Solars)
            total += P[i]
        P[0] = -1 * total
        for i in range(n):
            systems.append(theta[2 * i + 1])
            system = P[i] - gamma * theta[2 * i + 1]
            for j in range(n):
                system -= kappa * A[i,j] * np.sin(theta[2 * i] - theta[2 * j])
            systems.append(system)
        return systems
    t = np.linspace(0,tmax * 360 ,1000)
    sol = sp.odeint(dtheta,thetazero,t)
    if(drawGraph):
        plt.xticks([0,1*360,2*360,3*360,4*360,5*360,6*360,7*360,8*360,9*360,10*360,11*360,12*360,13*360,14*360,15*360,16*360,17*360,18*360,19*360,20*360,21*360,22*360,23*360,24*360],[0,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12])
        plt.plot(t,sol[:,2::2])
        plt.plot(t,sol[:,0],label = 'Grid usage')
        plt.legend()
        plt.xlim(0,24*360)
        plt.xlabel('time (AM/PM)')
        plt.ylabel(r'$\theta$ deviation of phase angle')
        plt.show()
    return sol

n = 10
Solars = SG.randomSolars(n,4)
Batteries = SG.randomSolars(n,4)
G = nx.watts_strogatz_graph(n, 4, 0.1) 
modelSystemFromSystem(n,Solars,G,True)