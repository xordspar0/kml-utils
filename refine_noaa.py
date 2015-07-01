######################################################################
# refine_noaa.py                                                     #
# Written by Jordan Christiansen                                     #
# Created: 23 June 2015                                              #
######################################################################
# Read a data from a CSV file from NOAA and output the data in       #
# another form.                                                      #
#                                                                    #
######################################################################

# TODO:
# Switch to using the Python CSV standard library.
# Optionally export to a database.
# Make some of the fields associated with an event optional.

import os.path
import sys

def main():
    if len(sys.argv) != 4:
        print_usage()

    # Check if the output file already exists
    if os.path.exists(sys.argv[3]):
        user_response = input(sys.argv[3] +
                ' already exists. Overwrite it? [y/N] ')
        if user_response == '' or user_response[0] != 'y':
            exit()

    #header = ('EVENT_ID\tLATITUDE\tLONGITUDE\t' + (46 * '{}\t') + '{}\n'
    #        ).format(*event_types)
    body = ''
    section = 49 * '{}\t' + '{}\n'

    # Parse the input files and build the string containing the body of the new
    # document as we go.
    with open(sys.argv[1]) as locations:
        for line in locations:
            line_fields = line.split(',')

            # Skip the line if it doesn't start with a number (this is for
            # skipping the header line)
            if not line_fields[0].isdigit():
                continue

            eventID = line_fields[2]
            latitude = line_fields[7]
            longitude = line_fields[8]
            this_event_type = find_event_type(line_fields[2])
            event_matrix = []
            
            for possible_event_type in event_types:
                if this_event_type.upper() == possible_event_type:
                    event_matrix.append(1)
                else:
                    event_matrix.append(0)

            body += section.format(eventID, latitude, longitude, *event_matrix)

    # Write the result to a file.
    with open(sys.argv[3], 'w') as output_file:
        output_file.write(header + body + footer)

def find_event_type(event_id):
    with open(sys.argv[2]) as details:
        for line in details:
            if event_id in line:
                return line.split(',')[12].strip('"')

def print_usage():
    print((
            'Usage: {} LOCATIONS_FILE DETAILS_FILE OUTPUT'
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
        'LAKESHORE FLOOD', 'LIGHTNING', 'MARINE HAIL', 'MARINE HIGH WIND',
        'MARINE STRONG WIND', 'MARINE THUNDERSTORM WIND', 'RIP CURRENT',
        'SEICHE', 'SLEET', 'STORM SURGE/TIDE', 'STRONG WIND', 'VOLCANIC ASH',
        'WATERSPOUT', 'WILDFIRE', 'WINTER STORM', 'WINTER WEATHER']

if __name__ == '__main__':
    main()

