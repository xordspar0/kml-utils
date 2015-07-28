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

def main():
    # Load the data.
    data = np.loadtxt('data/StormEvents_combined_d2010.csv', delimiter='\t')
    position = np.hstack((data[:, 2:3], data[:, 1:2]))
    categories = np.array(data[:, 3], dtype=np.int)
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

    # Take a random sample and perform an LDA analysis.
    np.random.seed(0)
    sample_size = 500
    sample_choice = np.random.choice(range(len(data)), size=sample_size)
    sample_pos = np.zeros((sample_size, 2))
    sample_cat = np.zeros(sample_size, np.int)
    sample_cat_counts = np.zeros(len(event_types), np.int)

    for i, choice in enumerate(sample_choice):
        sample_pos[i][0] = position[choice][0]
        sample_pos[i][1] = position[choice][1]
        sample_cat[i] = categories[choice]
        sample_cat_counts[categories[choice]] += 1

    # Plot the sample data.
    ax1 = plt.subplot2grid((2,2), (0,0),
            title='Random Sample (n={})'.format(sample_size))
    ax1.scatter(sample_pos[:, 0:1], sample_pos[:, 1:2], c=sample_cat)

    # Classify the data
    ldac()

    # Check the classification against the actual storm types.
    correct_total = 0
    # The positions of the correctly and incorrectly classified storms:
    correct_pos = []
    incorrect_pos = []
    # The evaluations array contains the total number of True Positives (0),
    # True Negatives (1), False Positives (2), and False Negatives (3) for each
    # event type:
    evaluations = np.zeros((len(event_types), 4), np.int)
    for i, classification in enumerate(classifications):
        if classification == sample_cat[i]:
            correct_total += 1
            correct_pos.append(sample_pos[i])
        else:
            incorrect_pos.append(sample_pos[i])

        # Positive
        for event_type_index, event_type in enumerate(event_types):
            if classification == event_type_index:
                # True
                if sample_cat[i] == event_type_index:
                    evaluations[event_type_index][0] += 1
                # False
                else:
                    evaluations[event_type_index][2] += 1
            # Negative
            else:
                # True
                if sample_cat[i] != event_type_index:
                    evaluations[event_type_index][1] += 1
                # False
                else:
                    evaluations[event_type_index][3] += 1

    correct_pos = np.array(correct_pos)
    incorrect_pos = np.array(incorrect_pos)
    evaluations = np.array(evaluations)

    # Plot the correctness data.
    ax2 = plt.subplot2grid((2,2), (0,1),
            title='Correct/Incorrect Classifications')
    ax2.scatter(incorrect_pos[:, 0:1], incorrect_pos[:, 1:2], c='b')
    ax2.scatter(correct_pos[:, 0:1], correct_pos[:, 1:2], c='y')
    ax2.legend(['incorrect', 'correct'])

    # Plot the True/False Positives/Negatives
    ax3 = plt.subplot2grid((2,2), (1,0), colspan=2,
            title='Classifications For Each Storm Type', xlim=[0,47])
    ax3.bar(range(47), evaluations[:, 0], color='blue')
    ax3.bar(range(47), evaluations[:, 2], bottom=evaluations[:, 0], color='red')
    ax3.bar(range(47), evaluations[:, 3], bottom=evaluations[:, 0] + evaluations[:, 2], color='yellow')
    ax3.bar(range(47), evaluations[:, 1], bottom=evaluations[:, 0] + evaluations[:, 2] + evaluations[:, 3], color='black')
    ax3.legend(['True Positives', 'False Positives', 'False Negatives', 'True Negatives'], loc=2)

    # Show result and graphs
    print('Sample size: {}'.format(sample_size))
    print('Number of total correct classifications: {} ({:.2%})'.format(
            correct_total, (correct_total/sample_size) ))
    print()
    for i, event_type in enumerate(event_types):
        if sample_cat_counts[i] > 0:
            print('Number of correct classifications for {}: {} ({:.2%})'.format(
                    event_type, evaluations[i][0],
                    (evaluations[i][0]/sample_cat_counts[i]) ))
    print()
    print('Storm types not listed were not present in the sample.')
    plt.show()

def lda():
    # Use mlpy's Linear Discriminant Analysis to learn and classify the data.
    ldac = mlpy.LDAC()
    ldac.learn(sample_pos, sample_cat)

    classifications = np.zeros(sample_size, np.int)
    for i, storm in enumerate(sample_pos):
        classifications[i] = ldac.pred(storm)

def knn():
    # Use mlpy's k-Nearest Neighbor to learn and classify the data.
    knn = mlpy.KNN(k=3)
    knn.learn(sample_pos, sample_cat)

    classifications = np.zeros(sample_size, np.int)
    for i, storm in enumerate(sample_pos):
        classifications[i] = knn.pred(storm)

main()
