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

usage_message = 'Usage: {} KML_File Output'.format(sys.argv[0])

if len(sys.argv) != 3:
    print(usage_message, file=sys.stderr)
    exit()

kml = ElementTree.parse(sys.argv[1])
coordinates = kml.findall('.//{http://www.opengis.net/kml/2.2}coordinates')

with open(sys.argv[2], 'w') as output_file:
    for coordinate in coordinates:
        longitude = coordinate.text.split(',')[0]
        latitude = coordinate.text.split(',')[1]
        #altitude = coordinate.text.split(',')[2]

        output_file.write(longitude + '\t' + latitude)

