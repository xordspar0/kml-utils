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
    if len(sys.argv) != 4:
        print_usage()

    # Check if the output file already exists
    if os.path.exists(sys.argv[3]):
        user_response = input(sys.argv[3] + ' already exists. Overwrite it? [y/N] ')
        if user_response == '' or user_response[0] != 'y':
            exit()

    # Strings containing the text of the resulting KML document.
    header  = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
               '<Folder>\n')
    body    =  ''
    section = ('\t<Placemark>\n'
               '\t\t<name>{}</name>\n'
               '\t\t<Point>\n'
               '\t\t\t<coordinates>{},{}</coordinates>\n'
               '\t\t</Point>\n'
               '\t</Placemark>\n')
    footer  = ('</Folder>\n'
               '</kml>\n')

    # Parse the input files and build the string containing the body of the KML
    # document as we go.
    with open(sys.argv[1]) as locations:
        for line in locations:
            line_fields = line.split(',')

            name = find_event_type(line_fields[2])
            latitude = line_fields[7]
            longitude = line_fields[8]

            body = body + section.format(name, longitude, latitude)

    # Write the resulting KML to a file.
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

if __name__ == '__main__':
    main()

