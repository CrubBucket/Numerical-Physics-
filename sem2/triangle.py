import numpy as np


class Triangle:

    def __init__(self, l):
        self.l = l
        self.x0, self.y0 = -l/2, -l * np.sqrt(3)/6
        self.x1, self.y1 = 0, l * np.sqrt(3)/3
        self.x2, self.y2 = l/2, -l * np.sqrt(3)/6

    def plot(self, ax, dim='3d'):
        x = [self.x0, self.x1, self.x2, self.x0]
        y = [self.y0, self.y1, self.y2, self.y0]
        if dim == '2d':
            ax.plot(x, y)
        else:
            z = np.zeros(4)
            ax.plot(x, y, z)


class Cylinder:

    def __init__(self, r, h):
        self.r = r
        self.h = h
        self.grid_size = 50

    def plot(self, ax, dim='3d'):
        if dim == '2d':
            theta = np.linspace(0, 2 * np.pi, self.grid_size)
            ax.plot(self.r * np.cos(theta), self.r * np.sin(theta))
        else:
            z = np.linspace(0, self.h, self.grid_size)
            theta = np.linspace(0, 2 * np.pi, self.grid_size)
            t_grid, z_grid = np.meshgrid(theta, z)
            x_grid = self.r * np.cos(t_grid)
            y_grid = self.r * np.sin(t_grid)
            ax.plot_surface(x_grid, y_grid, z_grid)


