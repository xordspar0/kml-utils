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
import matplotlib.patches as mpatches
import mlpy

# Load the data.
data = np.loadtxt('data/StormEvents_combined_d2010.csv', delimiter='\t')
position = np.hstack((data[:, 2:3], data[:, 1:2]))
categories = np.array(data[:, 3:4].flatten(), dtype=np.int)

# Plot all of the data.
ax1 = plt.subplot2grid((2,3), (0,0), rowspan=2, colspan=2,
        title='All Storms', aspect='equal')
ax1.scatter(position[:, 0:1], position[:, 1:2], c=categories)

# Take a random sample and perform an LDA analysis.
np.random.seed(0)
sample_size = 500
sample_choice = np.random.choice(range(len(data)), size=sample_size)
sample_pos = np.zeros((sample_size, 2))
sample_cat = np.zeros(sample_size, np.int)

for i, choice in enumerate(sample_choice):
    sample_pos[i][0] = position[choice][0]
    sample_pos[i][1] = position[choice][1]
    sample_cat[i] = categories[choice]

# Plot the sample data
ax2 = plt.subplot2grid((2,3), (0,2),
        title='Random Sample (n={})'.format(sample_size),
        aspect='equal', ylim=[-20,80])
ax2.scatter(sample_pos[:, 0:1], sample_pos[:, 1:2], c=sample_cat)

# Use mlpy's LDAC to learn and classify the data
ldac = mlpy.LDAC()
ldac.learn(sample_pos, sample_cat)

classifications = np.zeros(sample_size, np.int)
for i, storm in enumerate(sample_pos):
    classifications[i] = ldac.pred(storm)

# Check the classification against the actual storm types
correct = 0
incorrect = 0
correctness_matrix = []
for i in range(sample_size):
    if classifications[i] == sample_cat[i]:
        correct += 1
        correctness_matrix.append('b')
    else:
        incorrect += 1
        correctness_matrix.append('y')

ax3 = plt.subplot2grid((2,3), (1,2),
        title='Correct/Incorrect Classifications',
        aspect='equal', ylim=[-20,80])
ax3.scatter(sample_pos[:, 0:1], sample_pos[:, 1:2], c=correctness_matrix)
correct_key = mpatches.Patch(color='b', label='correct')
incorrect_key = mpatches.Patch(color='y', label='incorrect')
ax3.legend(handles = [correct_key, incorrect_key])

# Show results
print("Sample size: {}".format(sample_size))
print("Number of correct classifications: {} ({}%)".format(
        correct, (100*correct/sample_size) ))
print("Number of incorrect classifications: {} ({}%)".format(
        incorrect, (100*incorrect/sample_size) ))
plt.show()

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

