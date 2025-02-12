import numpy as np
import csv
import matplotlib.pyplot as plt

consumptionPoly = [ 1.04201341e-07, -8.94503881e-06,  2.98974192e-04, -4.88601783e-03, 3.98751419e-02, -1.43272977e-01,  1.36065097e-01,  2.63901363e-01]

def poly_eval(func,t):
    n = len(func)
    val = 0
    for i in range(n):
        val += func[i] * t ** (n - i - 1)
    return val

with open('Consumption_data.csv') as f:
    reader = csv.reader(f)
    data = list(reader)

data_array = np.array(data, dtype=float)
t = np.linspace(0,24,100)
plt.plot(data_array[::,0],data_array[::,1])
""" for i in range(30):
    func = np.polyfit(data_array[::,0],data_array[::,1],i)
    line = plt.plot(t,poly_eval(func,t),label = 'degree= ' + str(i))
    plt.xlim(0,23.5)
    plt.ylim(0,0.75)
    plt.draw()
    plt.legend()
    plt.pause(.5)
    line[0].remove() """
n = 7
func = np.polyfit(data_array[::,0],data_array[::,1],n)
line = plt.plot(t,poly_eval(func,t),label = 'degree= ' + str(n))
plt.xlim(0,23.5)
plt.ylim(0,0.75)
print(func)
plt.legend()
plt.show()