import numpy as np
import systemGenerators as SG
import matplotlib.pyplot as plt
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

t = np.linspace(0,24*360,1000)
n = 10
Solars = SG.randomSolars(n,4)
P = np.zeros(n)
y = np.zeros(1000)
y2 = np.zeros(1000)
y3 = np.zeros(1000)
for j in range(1000):
    total = 0
    for i in range(1,n):
        P[i] = netPower(t[j],i,Solars)
        total += P[i]
        if(Solars[i] == 1):
            y2[j] += getGen(t[j])
        y3[j] -= getCon(t[j])
    y[j] = -total
plt.plot(t,y,label = 'Input/Output from grid')
plt.plot(t,y2,label = 'Solar generation')
plt.plot(t,y3,label = 'Consumption')
plt.fill_between(
        x= t, 
        y1= 0, y2 = y,
        where= (7*360 < t)&(t < 17.2*360),
        color= "r",
        alpha= 0.4,label = 'Exporting')
plt.fill_between(
        x= t, 
        y1= y, y2 = 0,
        where= (7*360 > t)&(t>0),
        color= "g",
        alpha= 0.4,label = 'Importing')
plt.fill_between(
        x= t, 
        y1= y, y2 = 0,
        where= (17.2*360 < t)&(t < 24 * 360),
        color= "g",
        alpha= 0.4)
plt.hlines(0,0,24*360)
plt.xlim(0,24*360)
plt.legend()
plt.xticks([0,1*360,2*360,3*360,4*360,5*360,6*360,7*360,8*360,9*360,10*360,11*360,12*360,13*360,14*360,15*360,16*360,17*360,18*360,19*360,20*360,21*360,22*360,23*360,24*360],[0,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12])
plt.xlabel('time (AM/PM)')
plt.ylabel('Power (KW/H)')
plt.show()
plt.show()
