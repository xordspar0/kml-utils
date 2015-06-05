######################################################################
# noaa2kml.py                                                        #
# Written by Jordan Christiansen                                     #
# Created: 4 June 2015                                               #
######################################################################
# Read a list of geospactial coordinates from a CSV file from NOAA   #
# and translate it into a KML file.                                  #
#                                                                    #
######################################################################

import os.path
import re
import sys

def main():
    if len(sys.argv) != 3:
        print_usage()

    # Check if the output file already exists
    if os.path.exists(sys.argv[-1]):
        user_response = input(sys.argv[-1] + ' already exists. Overwrite it? [y/N] ')
        if user_response == '' or user_response[0] != 'y':
            exit()

    # Strings containing the text of the resulting KML document.
    header  = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
               '<Folder>\n')
    body    =  ''
    section = ('\t<Placemark>\n'
               '\t\t<Point>\n'
               '\t\t\t<coordinates>{},{}</coordinates>\n'
               '\t\t</Point>\n'
               '\t</Placemark>\n')
    footer  = ('</Folder>\n'
               '</kml>\n')

    # Parse the input files and build the string containing the body of the KML
    # document as we go.
    with open(sys.argv[1]) as input_file:
        for line in input_file:
            latitude = line.strip().split(',')[7]
            longitude = line.strip().split(',')[8]

            body = body + section.format(longitude, latitude)

    # Write the resulting KML to a file.
    with open(sys.argv[-1], 'w') as output_file:
        output_file.write(header + body + footer)

def print_usage():
    print((
            'Usage: {} NOAA_CSV_FILE OUTPUT'
            ).format(sys.argv[0]), file=sys.stderr)
    exit()

if __name__ == '__main__':
    main()

