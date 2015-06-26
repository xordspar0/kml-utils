######################################################################
# analyze_noaa.py                                                    #
# Written by Jordan Christiansen                                     #
# Created: 25 June 2015                                              #
######################################################################
# Analyze data from NOAA.                                            #
#                                                                    #
######################################################################

import statistics
import sys

def main():
    if len(sys.argv) != 2:
        print_usage()

    data = []

    with open(sys.argv[1]) as data_file:
        for line in data_file:
            line_fields = line.split()

            data.append(tuple(line_fields[1:-1]))

    sort(data)

def sort(data):
    for index, event_type in enumerate(event_types):
        with open(event_type, 'x') as csv_file:
            

def print_usage():
    print((
            'Usage: {} DATA_FILE'
            ).format(sys.argv[0]), file=sys.stderr)
    exit()

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

if __name__ == '__main__':
    main()

