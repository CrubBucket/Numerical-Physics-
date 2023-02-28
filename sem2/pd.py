import pandas as pd
from random import choice

data = pd.read_csv('sigmas.csv')

print(data.loc[data.E == 0.15, 'Compton'].iloc[0])

