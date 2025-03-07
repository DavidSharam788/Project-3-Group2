import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0.5,1.5,10)
y = [0.04124293785,0.07005649718,0.1717514124,0.3248587571,0.5576271186,0.7310734463,0.893785310,0.9322033898,0.9790960452,0.997740113]

plt.plot(x,y)
plt.ylabel("S")
plt.xlabel(r"$\alpha_c$")
plt.show()