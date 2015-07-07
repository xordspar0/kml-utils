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

data = np.loadtxt('data/StormEvents_combined_d2010.csv', delimiter='\t')

x = data[:, 2:3]
y = data[:, 1:2]
colors = data[:, 3:4]
plt.scatter(x, y, c=colors)
plt.show()

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

