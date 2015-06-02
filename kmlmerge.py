######################################################################
# kmlmerge.py                                                        #
# Written by Jordan Christiansen                                     #
# Created: 2 June 2015                                               #
######################################################################
# Combine multiple KML files into one.                               #
#                                                                    #
######################################################################

import os.path
import sys
from xml.etree import ElementTree

def main():
    if len(sys.argv) < 3:
        print_usage()

    # Check if the output file already exists
    if os.path.exists(sys.argv[-1]):
        user_response = input(sys.argv[-1] + ' already exists. Overwrite it? [y/N] ')
        if user_response == '' or user_response[0] != 'y':
            exit()

    # Parse each KML file to be merged
    elements = []
    for input_file in sys.argv[1:-1]:
        kml = ElementTree.parse(input_file)
        elements += list(kml.getroot())
    
    for element in elements:
        ElementTree.dump(element)

#    # Write the merged KML to a file
#    with open(sys.argv[-1], 'w') as output_file:
#        for coordinate in elements:
#            for coordinate_line in coordinate.text.strip().split('\n'):
#                split_coordinate = coordinate_line.strip().split(',')
#                output_string = ""
#                
#                if len(split_coordinate) >= 2:
#                    longitude = split_coordinate[0]
#                    latitude = split_coordinate[1]
#                    output_string += longitude + delimiter + latitude
#                if len(split_coordinate) >= 3:
#                    altitude = split_coordinate[2]
#                    output_string += delimiter + altitude
#
#                # Skip empty lines
#                if output_string != '':
#                    output_file.write(output_string + '\n')

def print_usage():
    print((
        'Usage: {} [-d=DELIM_CHAR] {{KML_FILE}} OUTPUT\n'
        'DELIM_CHAR can be a comma, tab, or space'
        ).format(sys.argv[0]), file=sys.stderr)
    exit()

if __name__ == '__main__':
    main()
