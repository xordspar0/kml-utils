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
    kml_document = ElementTree.ElementTree()
    kml_document._setroot(ElementTree.Element('kml'))
    root_folder = ElementTree.Element('Folder')
    kml_document.getroot().append(root_folder)
    for input_file in sys.argv[1:-1]:
        for element in list(ElementTree.parse(input_file).getroot()):
            root_folder.append(element)
    
    ElementTree.register_namespace('', 'http://www.opengis.net/kml/2.2')
    kml_document.write(sys.argv[-1], encoding='utf-8', xml_declaration=True)
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
        'Usage: {} {{KML_FILES}} OUTPUT'
        ).format(sys.argv[0]), file=sys.stderr)
    exit()

if __name__ == '__main__':
    main()
