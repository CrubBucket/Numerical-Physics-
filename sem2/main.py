import numpy as np
import matplotlib.pyplot as plt
from triangle import Triangle, Cylinder


tri = Triangle(l=30)
cyl = Cylinder(r=25, h=10)
ax = plt.axes(projection='3d')
tri.plot(ax)
cyl.plot(ax, dim='3d')
plt.show()
