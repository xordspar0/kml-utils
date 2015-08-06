######################################################################
# analyze_noaa.py                                                    #
# Written by Jordan Christiansen                                     #
# Created: 25 June 2015                                              #
######################################################################
# Analyze data from NOAA.                                            #
#                                                                    #
######################################################################

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import mlpy

SAMPLE_SIZE = 5000
MYCOLORS = ['DarkOrange','OliveDrab','Orchid','Orange','Peru','Turquoise',
            'LightBlue','DarkSeaGreen','Purple','Khaki','DarkSlateBlue',
            'LimeGreen','Pink','FireBrick','MidnightBlue','WhiteSmoke']
EVENT_TYPES = ['ASTRONOMICAL LOW TIDE', 'AVALANCHE', 'BLIZZARD',
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

def main():
    # Load the data.
    data = np.loadtxt('data/StormEvents_combined_d2010.csv', delimiter='\t')
    locations = np.hstack((data[:, 2:3], data[:, 1:2]))
    categories = np.array(data[:, 3], dtype=np.int)

    # Take a random sample and perform an LDA analysis.
    np.random.seed(0)
    sample_choice = np.random.choice(range(len(data)), size=SAMPLE_SIZE)
    sample_loc = np.zeros((SAMPLE_SIZE, 2))
    sample_cat = np.zeros(SAMPLE_SIZE, np.int)
    sample_cat_counts = np.zeros(len(EVENT_TYPES), np.int)

    for i, choice in enumerate(sample_choice):
        sample_loc[i][0] = locations[choice][0]
        sample_loc[i][1] = locations[choice][1]
        sample_cat[i] = categories[choice]
        sample_cat_counts[categories[choice]] += 1

    # Plot the sample data.
    ax1 = plt.subplot2grid((4,2), (0,0),
            title='Random Sample (n={})'.format(SAMPLE_SIZE))
    colormap = [MYCOLORS[x%len(MYCOLORS)] for x in sample_cat]
    ax1.scatter(sample_loc[:, 0:1], sample_loc[:, 1:2], c=colormap)

    # Classify the data
    classifications = ldac(sample_loc, sample_cat)

    # Check the classification against the actual storm types.
    correct_total = 0
    # The locations of the correctly and incorrectly classified storms:
    correct_loc = []
    incorrect_loc = []
    # The evaluations array contains the total number of True Positives (0),
    # True Negatives (1), False Positives (2), and False Negatives (3) for each
    # event type:
    evaluations = np.zeros((len(EVENT_TYPES), 4), np.int)
    for i, classification in enumerate(classifications):
        if classification == sample_cat[i]:
            correct_total += 1
            correct_loc.append(sample_loc[i])
        else:
            incorrect_loc.append(sample_loc[i])

        # Positive
        for event_type_index, event_type in enumerate(EVENT_TYPES):
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

    correct_loc = np.array(correct_loc)
    incorrect_loc = np.array(incorrect_loc)
    evaluations = np.array(evaluations)

    # Plot the correctness data.
    ax2 = plt.subplot2grid((4,2), (0,1),
            title='Correct/Incorrect Classifications')
    ax2.scatter(incorrect_loc[:, 0:1], incorrect_loc[:, 1:2], c='b')
    ax2.scatter(correct_loc[:, 0:1], correct_loc[:, 1:2], c='y')
    ax2.legend(['incorrect', 'correct'])

    # Plot the True/False Positives/Negatives.
    ax3 = plt.subplot2grid((4,2), (3,0), colspan=2,
            title='Classifications For Each Storm Type', xlim=[0,47])
    bar1 = ax3.bar(range(47), evaluations[:, 0], label='True Positives',
            color='cyan')
    bar2 = ax3.bar(range(47), evaluations[:, 3], label='False Negatives',
            color='purple', bottom=evaluations[:, 0])
    bar3 = ax3.bar(range(47), evaluations[:, 2], label='False Positives',
            color='gray', bottom=evaluations[:, 0] + evaluations[:, 3])
    bar4 = ax3.bar(range(47), evaluations[:, 1], label='True Negatives',
            color='black', bottom=(evaluations[:, 0] + evaluations[:, 3]
                + evaluations[:, 2]))
    handles, labels = ax3.get_legend_handles_labels()
    ax3.legend(handles[::-1], labels[::-1], loc=2)

    # Show result and graphs.
    print('Sample size: {}'.format(SAMPLE_SIZE))
    print('Number of total correct classifications: {} ({:.2%})'.format(
            correct_total, (correct_total/SAMPLE_SIZE) ))
    print()
    # Show stats for each storm type and do a chi-squared test.
    for i, event_type in enumerate(EVENT_TYPES):
        if sample_cat_counts[i] > 0:
            print('{} (#{}):'.format(event_type, i))
            print('\tTotal number: {}'.format(sample_cat_counts[i]))
            print('\tNumber correctly identified: {} ({:.2%})'.format(
                evaluations[i][0],
                (evaluations[i][0]/sample_cat_counts[i]) ))
            print(('\tIs the machine learning algorithm useful for this storm '
                'type? {}').format(chisq_test(sample_cat_counts[i],
                    evaluations[i][0]+evaluations[i][2])) )
    print()
    print('Storm types not listed were not present in the sample.')
    plt.show()

# Use mlpy's Linear Discriminant Analysis to learn and classify the data.
def ldac(locations, categories):
    ax = plt.subplot2grid((4,2), (1,0), colspan=2, rowspan=2,
            title='Classification Lines', xlim=[-180,-40], ylim=[10,70])

    ldac = mlpy.LDAC()
    ldac.learn(locations, categories)

    classifications = np.zeros(SAMPLE_SIZE, np.int)
    for i, storm in enumerate(locations):
        classifications[i] = ldac.pred(storm)

    # Plot the predictions.
    ## Map the categories to colors
    for event_type_index in range(len(EVENT_TYPES)):
        this_predicted_category = []
        for i in range(SAMPLE_SIZE):
            if classifications[i] == event_type_index:
                this_predicted_category.append(locations[i])
        if not this_predicted_category:
            continue
        this_predicted_category = np.array(this_predicted_category)
        ax.scatter(this_predicted_category[:, 0], this_predicted_category[:, 1],
                label=EVENT_TYPES[event_type_index],
                c=MYCOLORS[event_type_index%len(MYCOLORS)])

    ax.legend(loc=2)

    x = np.arange(-180,-40)
    w = ldac.w()
    b = ldac.bias()
    for i in range(len(w)):
        for j in range(len(w)):
            if i == j:
                break
            y = (x* (w[j][0] - w[i][0]) + b[j] - b[i]) / (w[i][1] - w[j][1])
            ax.plot(x,y,'k--')

    return classifications

# Use mlpy's k-Nearest Neighbor to learn and classify the data.
def knn(locations, categories):
    knn = mlpy.KNN(k=3)
    knn.learn(locations, categories)

    classifications = np.zeros(SAMPLE_SIZE, np.int)
    for i, storm in enumerate(locations):
        classifications[i] = knn.pred(storm)

    return classifications

# This is a chi-squared test to see if the classification of our machine
# learning algorithm was useful.
# The null hypothesis is that there is no significant difference between the
#   algorithm's classification and the actual category each storm belongs to.
# The alternative hypythesis is that there is a difference, which would make
#   the algorithm useless.
def chisq_test(actually_true, predicted_true):
    alpha = 0.05 # significance level
    # Calculate the totals.
    total = SAMPLE_SIZE * 2
    total_true = actually_true + predicted_true
    total_false = (SAMPLE_SIZE - actually_true) + (SAMPLE_SIZE - predicted_true)

    # Calculate the expected values.
    expected_ratio_true = total_true / total
    expected_actually_true = expected_ratio_true * SAMPLE_SIZE
    expected_actually_false = SAMPLE_SIZE - expected_ratio_true * SAMPLE_SIZE
    expected_predicted_true = expected_ratio_true * SAMPLE_SIZE
    expected_predicted_false = SAMPLE_SIZE - expected_ratio_true * SAMPLE_SIZE

    # Calculate the test statistic.
    chisquared = ( (actually_true - expected_actually_true)**2 / expected_actually_true
            + (predicted_true - expected_predicted_true)**2 / expected_predicted_true
            + (SAMPLE_SIZE - actually_true - expected_actually_false)**2 / expected_actually_false
            + (SAMPLE_SIZE - predicted_true - expected_predicted_false)**2 / expected_predicted_false )

    # Get the p-value.
    pvalue = stats.chi2.sf(chisquared, df=1)

    # FYI. I'm not sure if this should be in the output or not.
    print('\tchi-squared statistic: {:.3f}'.format(chisquared))
    print('\tp-value: {:.3f}'.format(pvalue))

    #   If the p-value is large, we accept the null hypothesis that there is no
    # difference between the predicted and actual storm category, which means
    # that the machine learning algorithm IS USEFUL for the type of storm.
    #   If the p-value is small, we reject the null hypothesis and say that
    # there is a difference, which means that the machine learning algorithm is
    # NOT USEFUL for this type of storm.
    return pvalue > alpha
main()
