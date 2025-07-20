#visualize derivatives in Python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def expr(x):
    return x**2

def expr_der(x):
    return 2*x

values = np.linspace(-10, 10, 100) #Create value for function

plt.plot(values, expr(values))

x1 = -5
y1 = expr(x1)

xrange = np.linspace(x1 - 5, x1 + 5, 10)

#Define Tangent line
def line (x, x1, y1):
    return expr_der(x1)*(x-x1) + y1

plt.plot(xrange, line(xrange, x1, y1), '--')
plt.scatter(x1, y1, s=50, c='C1')
plt.show()