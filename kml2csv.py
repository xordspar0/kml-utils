######################################################################
# kml2csv.py                                                         #
# Written by Jordan Christiansen                                     #
# Created: 22 May 2015                                               #
######################################################################
# Read a KML file and translate it into delimited text.              #
#                                                                    #
######################################################################

import os.path
import sys
from xml.etree import ElementTree

def main():
    if len(sys.argv) < 3:
        print_usage()

    # Set the delimiter for the delimited text file based on the -d option
    # first_file_arg is the argument where the first file should be found.
    # The -d=, and -d , syntaxes are both acceptable
    if sys.argv[1] == '-d':
        delimiter = sys.argv[2]
        first_file_arg = 3
    elif sys.argv[1].startswith('-d=') and len(sys.argv[1]) == 4:
        delimiter = sys.argv[1].split('=')[1]
        first_file_arg = 2
    else:
        delimiter = '\t'
        first_file_arg = 1

    # Make sure that the delimiter is a reasonable character
    if not delimiter in [',', '\t', ' ']:
        print_usage()

    # If there aren't enough file arguments, display the usage message and exit.
    if len(sys.argv) < 2 + first_file_arg:
        print_usage()

    # Check if the output file already exists
    if os.path.exists(sys.argv[-1]):
        user_response = input(sys.argv[-1] + ' already exists. Overwrite it? [y/N] ')
        if user_response == '' or user_response[0] != 'y':
            exit()

    # Parse each KML file and look for <coordinates> tags in each file.
    coordinates = []
    for input_file in sys.argv[first_file_arg:-1]:
        kml = ElementTree.parse(input_file)
        coordinates += kml.findall(
                './/{http://www.opengis.net/kml/2.2}coordinates')

    # Write the coordinates to a file as delimited text
    with open(sys.argv[-1], 'w') as output_file:
        for coordinate in coordinates:
            output_string = ""
            split_coordinates = coordinate.text.strip().split(',')
            
            if len(split_coordinates) >= 2:
                longitude = split_coordinates[0]
                latitude = split_coordinates[1]
                output_string += longitude + delimiter + latitude
            if len(split_coordinates) >= 3:
                altitude = split_coordinates[2]
                output_string += delimiter + altitude

            # Skip empty lines
            if output_string != '':
                output_file.write(output_string + '\n')

def print_usage():
    print((
        'Usage: {} [-d=DELIM_CHAR] {{KML_FILE}} OUTPUT\n'
        'DELIM_CHAR can be a comma, tab, or space'
        ).format(sys.argv[0]), file=sys.stderr)
    exit()

if __name__ == '__main__':
    main()
