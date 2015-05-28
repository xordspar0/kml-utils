######################################################################
# kml2csv.py                                                         #
# Written by Jordan Christiansen                                     #
# Created: 22 May 2015                                               #
######################################################################
# Read a KML file and translate it into delimited text.              #
#                                                                    #
######################################################################

import sys
from xml.etree import ElementTree

usage_message = 'Usage: {} {{KML_FILE}} OUTPUT'.format(sys.argv[0])

if len(sys.argv) < 3:
    print(usage_message, file=sys.stderr)
    exit()

coordinates = []
for input_file in sys.argv[1:-1]:
    kml = ElementTree.parse(input_file)
    coordinates += kml.findall('.//{http://www.opengis.net/kml/2.2}coordinates')

with open(sys.argv[-1], 'w') as output_file:
    for coordinate in coordinates:
        output_string = ""
        split_coordinates = coordinate.text.strip().split(',')
        
        if len(split_coordinates) >= 2:
            longitude = split_coordinates[0]
            latitude = split_coordinates[1]
            output_string += longitude + '\t' + latitude
        if len(split_coordinates) >= 3:
            altitude = split_coordinates[2]
            output_string += '\t' + altitude

        output_file.write(output_string + '\n')

