######################################################################
# csv2kml.py                                                         #
# Written by Jordan Christiansen                                     #
# Created: 21 May 2015                                               #
######################################################################
# Read a list of global coordinates from a CSV file and              #
# translates it into a KML file.                                     #
#                                                                    #
######################################################################

## TODO:
# Use an XML library to emit the KML document rather than plain strings.
#
# Possible future feature: convert the coordinates to things other than
# Placemarks (e.g. paths).
##

import sys

# The text of the resulting KML document.
header = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
          '<Folder>\n')
body = ''
footer = ('</Folder>\n'
          '</kml>\n')

for input_file in sys.argv[1:]:
    with open(input_file) as csv_file:
        for line in csv_file:

            longitude = line.split('\t')[0]
            latitude = line.split('\t')[1]

            body = body + (('\t<Placemark>\n'
                            '\t\t<Point>\n'
                            '\t\t\t<coordinates>{0},{1}</coordinates\n'
                            '\t\t</Point>\n'
                            '\t</Placemark>\n'
                            ).format(longitude, latitude))

print(header + body + footer)
        
