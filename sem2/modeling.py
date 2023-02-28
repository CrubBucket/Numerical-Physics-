import pandas as pd
import numpy as np


class Modeling:

    def __init__(self, source, surface, ax, min_energy):
        self.spectra = pd.read_csv('./sigmas.csv')
        self.photons = []
        self.dead_photons = []
        self.source = source
        self.surface = surface
        self.ax = ax
        self.min_energy = min_energy

    def generate_photons(self, n):
        for _ in range(n):
            index = np.random.randint(0, 18)
            photon = self.source.generate_photon(energy=self.spectra.loc[index, 'E'],
                                                            sigmas=(self.spectra.loc[index, 'Compton'],
                                                                    self.spectra.loc[index, 'Photo'],
                                                                    self.spectra.loc[index, 'Pair']))
            if self.surface.is_in(photon.last_position):
                self.photons.append(photon)

    def set_interactions(self):
        for i, photon in enumerate(self.photons):
            if photon.cast_next_interaction(min_energy=self.min_energy, spectra=self.spectra):
                if not self.surface.is_in(photon.last_position):
                    photon.delete_last_position()
                    self.dead_photons.append(photon)
                    del self.photons[i]
            else:
                self.dead_photons.append(photon)
                del self.photons[i]

        print(f'{len(self.photons)} are in area')

    def plot(self):
        self.source.plot(ax=self.ax)
        self.surface.plot(ax=self.ax)
        for photon in self.dead_photons:
            photon.plot_trajectory(ax=self.ax)

    @property
    def photons_alive(self):
        return len(self.photons)
