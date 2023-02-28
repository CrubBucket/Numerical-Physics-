import numpy as np
from photon import Photon


class Triangle:

    def __init__(self, l):
        self.l = l
        self.x0, self.y0 = -l/2, -l * np.sqrt(3)/6
        self.x1, self.y1 = 0, l * np.sqrt(3)/3
        self.x2, self.y2 = l/2, -l * np.sqrt(3)/6
        self.angle = np.pi / 3

    def plot(self, ax, dim='3d'):
        x = [self.x0, self.x1, self.x2, self.x0]
        y = [self.y0, self.y1, self.y2, self.y0]
        if dim == '2d':
            ax.plot(x, y)
        else:
            z = np.zeros(4)
            ax.plot(x, y, z)

    def generate_photon(self, energy, sigmas):

        r1 = np.random.uniform(0, self.l)
        r2 = np.random.uniform(0, self.l)

        k = (self.y2 - self.y1) / (self.x2 - self.x1)
        b = (self.y1 - self.y0) - k * (self.x1 - self.x0)

        y_toss = r1 * np.sin(self.angle)
        x_toss = r2 + r1 * np.cos(self.angle)

        if y_toss > k * x_toss + b:
            y_mirr = self.l * np.sin(self.angle) - y_toss
            x_mirr = self.l * (1 + np.cos(self.angle)) - x_toss
            return Photon(birth_place=(x_mirr + self.x0, y_mirr + self.y0, 0), energy=energy, sigmas=sigmas)

        return Photon(birth_place=(x_toss + self.x0, y_toss + self.y0, 0), energy=energy, sigmas=sigmas)


class Cylinder:

    def __init__(self, r, h):
        self.r = r
        self.h = h
        self.grid_size = 50

    def is_in(self, coords):
        x, y, z = coords
        if (z > self.h) or (x**2 + y**2 > self.r**2) or (z < 0):
            return 0
        return 1

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
            ax.plot_surface(x_grid, y_grid, z_grid, color='grey', alpha=0.2)


