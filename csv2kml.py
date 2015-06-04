######################################################################
# csv2kml.py                                                         #
# Written by Jordan Christiansen                                     #
# Created: 21 May 2015                                               #
######################################################################
# Read a list of global coordinates from a CSV file and translate it #
# into a KML file.                                                   #
#                                                                    #
######################################################################

import os.path
import re
import sys

def main():
    if len(sys.argv) < 3:
        print_usage()

    # Determine the type of KML element based on the -t option
    # first_file_arg is the argument where the first file should be found.
    # The -t=path and -t path syntaxes are both acceptable
    if sys.argv[1] == '-t':
        kml_type = sys.argv[2]
        first_file_arg = 3
    elif sys.argv[1].startswith('-t='):
        kml_type = sys.argv[1].split('=')[1]
        first_file_arg = 2
    else:
        kml_type = 'placemark'
        first_file_arg = 1

    # Make sure the KML type is valid
    if not kml_type in ['placemark', 'path']:
        print_usage()

    # If there aren't enough file arguments, display the usage message and exit.
    if len(sys.argv) < 2 + first_file_arg:
        print_usage()

    # Check if the output file already exists
    if os.path.exists(sys.argv[-1]):
        user_response = input(sys.argv[-1] + ' already exists. Overwrite it? [y/N] ')
        if user_response == '' or user_response[0] != 'y':
            exit()

    # Strings containing the text of the resulting KML document.
    if kml_type == 'placemark':
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

    elif kml_type == 'path':
        header  = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
                   '<Placemark>\n'
                   '\t<LineString>\n'
                   '\t\t<extrude>0</extrude>\n'
                   '\t\t<tessellate>1</tessellate>\n'
                   '\t\t<altitudeMode>clampToGround</altitudeMode>\n'
                   '\t\t<coordinates>\n')
        body    =  ''
        section = ('\t\t\t{},{}\n')
        footer  = ('\t\t</coordinates>\n'
                   '\t</LineString>\n'
                   '</Placemark>\n'
                   '</kml>\n')

    # Regular expressions for parsing the CSV file.
    # Note that the delimiter can be a tab, a comma, or whitespace.
    decimal = '-?[0-9]+(.[0-9]+)?'
    delimiter = '[\t,]'
    line_validation = re.compile(decimal + delimiter + decimal)
    splitter = re.compile(delimiter)

    # Parse the input files and build the string containing the body of the KML
    # document as we go.
    for input_file in sys.argv[first_file_arg:-1]:
        with open(input_file) as current_file:
            for line in current_file:
                if (line_validation.match(line)):

                    longitude = splitter.split(line.strip())[0]
                    latitude = splitter.split(line.strip())[1]

                    body = body + section.format(longitude, latitude)

    # Write the resulting KML to a file.
    with open(sys.argv[-1], 'w') as output_file:
        output_file.write(header + body + footer)

def print_usage():
    print((
            'Usage: {} [-t=TYPE] {{CSV_FILE}} OUTPUT\n'
            'TYPE can be "placemark" or "path"'
            ).format(sys.argv[0]), file=sys.stderr)
    exit()

if __name__ == '__main__':
    main()

