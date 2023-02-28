import numpy as np
import matplotlib.pyplot as plt
from geometry import Triangle, Cylinder
from modeling import Modeling

tri = Triangle(l=30)
cyl = Cylinder(r=25, h=10)
ax = plt.axes(projection='3d')
modeling = Modeling(source=tri, surface=cyl, ax=ax, min_energy=0.02)
modeling.generate_photons(500)
while modeling.photons_alive:
    modeling.set_interactions()
modeling.plot()
plt.show()
