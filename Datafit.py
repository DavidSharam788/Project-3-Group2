import numpy as np
import csv
import matplotlib.pyplot as plt

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