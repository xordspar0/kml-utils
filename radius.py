#!/usr/bin/env python3

def application(environ, start_response):
    output_kml = kml_radius(40, -100, 5)

    status = '200 OK'
    response_headers = [('Content-Type', 'application/vnd.google-earth.kml+xml; charset=utf-8'),
                        ('Content-Length', str(len(output_kml)))]
    start_response(status, response_headers)

    return [output_kml]

def kml_radius(lat, lon, radius):
    from math import sin, cos, pi
    from random import random

    angle = random() * pi
    latitude = lat + radius * sin(angle)
    longitude = lon + radius * cos(angle)

    kml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
            '<Placemark>\n'
            '<name>5 Degrees Away</name>\n'
            '<Point>\n'
            '<coordinates>{0},{1},0</coordinates>\n'
            '</Point>\n'
            '</Placemark>\n'
            '</kml>'
            ).format(longitude, latitude).encode('utf-8')

    return kml
