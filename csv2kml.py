######################################################################
# csv2kml.py                                                         #
# Written by Jordan Christiansen                                     #
# Created: 21 May 2015                                               #
######################################################################
# Read a list of global coordinates from a CSV file and translate it #
# into a KML file.                                                   #
#                                                                    #
######################################################################

## TODO:
# Possible future feature: convert the coordinates to things other than
# Placemarks (e.g. paths).
##

import re
import sys

usage_message = 'Usage: {} {{CSV_FILE}} OUTPUT'.format(sys.argv[0])

if len(sys.argv) < 3:
    print(usage_message, file=sys.stderr)
    exit()

# The text of the resulting KML document.
header = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
          '<Folder>\n')
body = ''
footer = ('</Folder>\n'
          '</kml>\n')

# Regular expressions for parsing the CSV file.
# Note that the delimiter can be a tab, a comma, or whitespace.
decimal = '-?[0-9]+(.[0-9]+)?'
delimiter = '[\t, +]'
line_validation = re.compile(decimal + delimiter + decimal)
splitter = re.compile(delimiter)

for input_file in sys.argv[1:-1]:
    with open(input_file) as current_file:
        for line in current_file:
            if (line_validation.match(line)):

                longitude = splitter.split(line)[0]
                latitude = splitter.split(line)[1]

                body = body + ('\t<Placemark>\n'
                               '\t\t<Point>\n'
                               '\t\t\t<coordinates>{0},{1}</coordinates>\n'
                               '\t\t</Point>\n'
                               '\t</Placemark>\n'
                               ).format(longitude, latitude)

with open(sys.argv[-1], 'x') as output_file:
    output_file.write(header + body + footer)

