######################################################################
# analyze_noaa.py                                                    #
# Written by Jordan Christiansen                                     #
# Created: 25 June 2015                                              #
######################################################################
# Analyze data from NOAA.                                            #
#                                                                    #
######################################################################

import numpy as np
import matplotlib.pyplot as plt
import mlpy

# Load the data.
data = np.loadtxt('data/StormEvents_combined_d2010.csv', delimiter='\t')
x = data[:, 2:3].flatten()
y = data[:, 1:2].flatten()
categories = np.array([int(cat) for cat in data[:, 3:4].flat])

# Show all of the data.
plt.scatter(x, y, c=categories)
plt.show()

# Take a random sample and perform an LDA analysis.
np.random.seed(0)
sample_size = 500
sample_choice = np.random.random_integers(0, len(data), size=sample_size)
sample_x = np.empty(sample_size)
sample_y = np.empty(sample_size)
sample_cat = np.empty(sample_size, np.int)

for i, choice in enumerate(sample_choice):
    sample_x[i] = x[choice]
    sample_y[i] = y[choice]
    sample_cat[i] = categories[choice]

plt.scatter(sample_x, sample_y, c=sample_cat)
plt.show()

ldac = mlpy.LDAC()
ldac.learn([sample_x, sample_y], sample_cat)
    # [sample_x, sample_y] is rotated incorrectly. Its shape is (2, 500). I
    # need to figure out how to get an array with shape (500, 2) where x and y
    # are side by side.

for storm in sample:
    ldac.pred([sample_x, sample_y])

# Might need this later
event_types = ['ASTRONOMICAL LOW TIDE', 'AVALANCHE', 'BLIZZARD',
        'COASTAL FLOOD', 'COLD/WIND CHILL', 'DEBRIS FLOW', 'DENSE FOG',
        'DENSE SMOKE', 'DROUGHT', 'DUST DEVIL', 'DUST STORM', 'EXCESSIVE HEAT',
        'EXTREME COLD/WIND CHILL', 'FLASH FLOOD', 'FLOOD', 'FROST/FREEZE',
        'FUNNEL CLOUD', 'FREEZING FOG', 'HAIL', 'THUNDERSTORM WIND', 'TORNADO',
        'TROPICAL DEPRESSION', 'TROPICAL STORM', 'TSUNAMI', 'HEAT',
        'HEAVY RAIN', 'HEAVY SNOW', 'HIGH SURF', 'HIGH WIND',
        'HURRICANE (TYPHOON)', 'ICE STORM', 'LAKE-EFFECT SNOW',
        'LAKESHORE FLOOD', 'LIGHTNING', 'MARINE HAIL MARINE HIGH WIND',
        'MARINE STRONG WIND', 'MARINE THUNDERSTORM WIND', 'RIP CURRENT',
        'SEICHE', 'SLEET', 'STORM SURGE/TIDE', 'STRONG WIND', 'VOLCANIC ASH',
        'WATERSPOUT', 'WILDFIRE', 'WINTER STORM', 'WINTER WEATHER']

