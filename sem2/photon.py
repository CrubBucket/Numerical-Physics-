import numpy as np


class Photon:

    def __init__(self, birth_place, energy, sigmas):
        self.x_birth, self.y_birth, self.z_birth = birth_place
        self.energy = energy
        self.compton_sigma, self.photo_sigma, self.pair_sigma = sigmas
        self.mileage = - np.log(np.random.uniform()) / (self.compton_sigma + self.photo_sigma + self.pair_sigma)

        theta = Photon.get_theta()
        psi = Photon.get_psi()

        self.omegas = [np.cos(theta) * psi[1], np.cos(theta) * psi[0], np.sin(theta)]

        self.interaction_coords = []
        self.interaction_coords.append(birth_place)

        x_act = self.x_birth + self.mileage * self.omegas[0]
        y_act = self.y_birth + self.mileage * self.omegas[1]
        z_act = self.z_birth + self.mileage * self.omegas[2]
        self.interaction_coords.append((x_act, y_act, z_act))

        self.weight = 1.0
        self.mu = 1
        self.mc2 = 0.511

    @staticmethod
    def get_theta(): return np.arccos(2 * np.random.uniform() - 1)

    @staticmethod
    def get_psi():
        while True:
            a = 2 * np.random.uniform() - 1
            b = 2 * np.random.uniform() - 1
            d = a**2 + b**2
            if d <= 1:
                break
        return b / np.sqrt(d), a / np.sqrt(d)  # sin, cos

    def p(self, x, a_old): return x / a_old + a_old / x + (1 / a_old - 1 / x) * (2 + 1 / a_old - 1 / x)

    def cast_next_interaction(self, min_energy,  spectra):

        sigma_total = self.photo_sigma + self.pair_sigma + self.compton_sigma

        if self.compton_sigma / sigma_total <= np.random.uniform() or self.weight <= 1e-11 or min_energy > self.energy:
            return False

        self.weight *= self.compton_sigma / sigma_total
        a_old = self.energy / self.mc2

        while True:
            g1 = np.random.uniform()
            g2 = np.random.uniform()
            a = a_old * (1 + 2 * a_old * g1) / (1 + 2 * a_old)
            if g2 * (1 + 2 * a_old + 1 / (1 + 2 * a_old)) < self.p(a, a_old):
                break

        self.mu = 1 - 1 / a + 1 / a_old
        sin_psi, cos_psi = self.get_psi()

        energy_photon = a_old * self.mc2 / (1 + a_old * (1 - self.mu))
        self.energy = spectra.loc[spectra.E <= energy_photon, 'E'].iloc[-1]
        self.compton_sigma, self.photo_sigma, self.pair_sigma = (spectra.loc[spectra.E == self.energy, 'Compton'].iloc[0],
                                                                 spectra.loc[spectra.E == self.energy, 'Photo'].iloc[0],
                                                                 spectra.loc[spectra.E == self.energy, 'Pair'].iloc[0])

        omega1_ = self.omegas[0]
        omega2_ = self.omegas[1]
        omega3_ = self.omegas[2]

        omega3 = omega3_ * self.mu + np.sqrt((1 - self.mu * self.mu) * (1 - omega3_ * omega3_)) * cos_psi
        omega2 = (omega2_ * (self.mu - omega3_ * omega3) +
                  omega1_ * sin_psi * np.sqrt((1 - self.mu * self.mu) * (1 - omega3_ * omega3_))) / (1 - omega3_ * omega3_)
        omega1 = (omega1_ * (self.mu - omega3_ * omega3) -
                  omega2_ * sin_psi * np.sqrt((1 - self.mu * self.mu) * (1 - omega3_ * omega3_))) / (1 - omega3_ * omega3_)

        self.omegas[0] = omega1
        self.omegas[1] = omega2
        self.omegas[2] = omega3

        self.mileage = - np.log(np.random.uniform()) / (self.compton_sigma + self.photo_sigma + self.pair_sigma)
        r = self.mileage

        x_old, y_old, z_old = self.interaction_coords[-1]

        x_act = x_old + r * self.omegas[0]
        y_act = y_old + r * self.omegas[1]
        z_act = z_old + r * self.omegas[2]

        self.interaction_coords.append((x_act, y_act, z_act))

        return True

    def plot_trajectory(self, ax):
        xs = []
        ys = []
        zs = []

        for x, y, z in self.interaction_coords:
            xs.append(x)
            ys.append(y)
            zs.append(z)

        ax.plot(xs, ys, zs)

    @property
    def last_position(self): return self.interaction_coords[-1]

    def delete_last_position(self):
        self.interaction_coords = self.interaction_coords[:-1]



