import numpy as np
import pylab as pl
 
x = np.random.uniform(1, 100, 1000)
y = np.log(x) + np.random.normal(0, .3, 1000)
 
print pl.scatter(x, y, s=1, label="log(x) with noise")
print pl.plot(np.arange(1, 100), np.log(np.arange(1, 100)), c="b", label="log(x) true function")
print pl.xlabel("x")
print pl.ylabel("f(x) = log(x)")
print pl.legend(loc="best")
print pl.title("A Basic Log Function")
pl.show()