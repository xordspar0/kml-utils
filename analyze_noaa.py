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
position = np.hstack((data[:, 2:3], data[:, 1:2]))
categories = np.array(data[:, 3:4].flatten(), dtype=np.int)

# Show all of the data.
plt.scatter(position[:, 0:1], position[:, 1:2], c=categories)
plt.show()

# Take a random sample and perform an LDA analysis.
np.random.seed(0)
sample_size = 500
sample_choice = np.random.random_integers(0, len(data), size=sample_size)
sample_pos = np.zeros(position.shape)
sample_cat = np.zeros(categories.shape, np.int)

for i, choice in enumerate(sample_choice):
    sample_pos[i][0] = position[choice][0]
    sample_pos[i][1] = position[choice][1]
    sample_cat[i] = categories[choice]

plt.scatter(sample_pos[:, 0:1], sample_pos[:, 1:2], c=sample_cat)
plt.show()

ldac = mlpy.LDAC()
ldac.learn(sample_pos, sample_cat)

for storm in sample_pos:
    ldac.pred(storm)

# Might need this later
event_types = ['ASTRONOMICAL LOW TIDE', 'AVALANCHE', 'BLIZZARD',
        'COASTAL FLOOD', 'COLD/WIND CHILL', 'DEBRIS FLOW', 'DENSE FOG',
        'DENSE SMOKE', 'DROUGHT', 'DUST DEVIL', 'DUST STORM', 'EXCESSIVE HEAT',
        'EXTREME COLD/WIND CHILL', 'FLASH FLOOD', 'FLOOD', 'FROST/FREEZE',
        'FUNNEL CLOUD', 'FREEZING FOG', 'HAIL', 'HEAT', 'HEAVY RAIN',
        'HEAVY SNOW', 'HIGH SURF', 'HIGH WIND', 'HURRICANE (TYPHOON)',
        'ICE STORM', 'LAKE-EFFECT SNOW', 'LAKESHORE FLOOD', 'LIGHTNING',
        'MARINE HAIL MARINE HIGH WIND', 'MARINE STRONG WIND',
        'MARINE THUNDERSTORM WIND', 'RIP CURRENT', 'SEICHE', 'SLEET',
        'STORM SURGE/TIDE', 'STRONG WIND', 'THUNDERSTORM WIND', 'TORNADO',
        'TROPICAL DEPRESSION', 'TROPICAL STORM', 'TSUNAMI', 'VOLCANIC ASH',
        'WATERSPOUT', 'WILDFIRE', 'WINTER STORM', 'WINTER WEATHER']

