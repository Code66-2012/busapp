#!/usr/bin/env python
# vim: ts=4 sw=4 et

from __future__ import unicode_literals

import json
import re

import bottle
import requests

from bottle import route, debug, response
from lxml import etree


headers = {'user-agent': 'Code 66 hackathon'}
namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}

@route('/')
@route('/nyan') # backward compatibility, remove this
def go():
    response.content_type = 'application/json'

    session = requests.session(headers=headers)

    d = session.get('http://data.cabq.gov/transit/realtime/introute/intallbuses.kml')
    stops = session.get('http://data.cabq.gov/transit/routesandstops/transitstops.kmz')
    raw_document = d.content

    raw_document = file('tests/intallbuses.kml').read()

    try:
        raw_document = raw_document.encode('utf-8')
    except UnicodeDecodeError:
        pass

    t = etree.fromstring(raw_document)

    bus_elements = t.xpath('//kml:Placemark', namespaces=namespaces)
    bus_elements_output = []
    for bus_element in bus_elements:
        r = {}

        # Bus ID
        bus_id = bus_element.xpath('kml:name', namespaces=namespaces)[0].text
        r['bus_id'] = bus_id

        # Route ID
        route_id = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[text()="Route"]/following-sibling::*', namespaces=namespaces)
        if not route_id:
            continue
        route_id = route_id[0].text
        if route_id == 'Off Duty':
            continue
        r['route_id'] = route_id

        # Next Stop
        next_stop = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[normalize-space(text())="Next Stop"]/following-sibling::*', namespaces=namespaces)[0].text
        next_stop = re.match('(.*) @(.*) scheduled', next_stop)
        if next_stop:
            next_stop = next_stop.groups()
            next_stop = [i.strip() for i in next_stop]
        else:
            print next_stop
        r['next_stop'] = next_stop

        # Speed
        speed = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[text()="Speed"]/following-sibling::*', namespaces=namespaces)[0].text
        speed = speed.split()[0]
        r['speed'] = float(speed)

        # Message Time
        msg_time = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[text()="Msg Time"]/following-sibling::*', namespaces=namespaces)[0].text
        r['msg_time'] = msg_time

        # Coordinates
        coords = bus_element.xpath('kml:Point/kml:coordinates', namespaces=namespaces)[0].text
        coords = coords.split(',')
        coords_out = {}
        coords_out['lon'] = float(coords[0])
        coords_out['lat'] = float(coords[1])
        r['coords'] = coords_out

        bus_elements_output.append(r)
    return json.dumps(bus_elements_output)

application = bottle.default_app()


if __name__ == '__main__':
#    import pprint
#    pprint.pprint(go())
    from bottle import run
    debug(True)
    run(reloader=True)
