#!/usr/bin/env python
# vim: ts=4 sw=4 et

from __future__ import unicode_literals

import bottle
from bottle import route, debug, response
import json
import requests
from lxml import etree
import re
import zipfile
from StringIO import StringIO

headers = {'user-agent': 'Code 66 hackathon'}
namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}

@route('/')
@route('/nyan') # backward compatibility, remove this
def go():
    response.content_type = 'application/json'

    session = requests.session(headers=headers)

    d = session.get('http://data.cabq.gov/transit/realtime/introute/intallbuses.kml')
    stops = session.get('http://data.cabq.gov/transit/routesandstops/transitstops.kmz')
    #stops = session.get('http://web.localhost/transitstops.kmz')
    raw_document = d.content
    raw_stops = stops
    raw_stops = stops.content

    raw_document = file('tests/intallbuses.kml').read()

    try:
        raw_document = raw_document.encode('utf-8')
        #raw_stops = raw_stops.encode('utf-8')
    except UnicodeDecodeError:
        pass
    raw_stops = zipfile.ZipFile(StringIO(raw_stops), 'r')
    raw_stops = raw_stops.open('doc.kml').read()

    raw_stops = raw_stops.replace('http://earth.google.com/kml/2.2', namespaces['kml'])
    t = etree.fromstring(raw_document)
    st = etree.fromstring(raw_stops)
    stop_elements = st.xpath('//kml:Placemark', namespaces=namespaces)
    stop_elements_output = []
    for stop in stop_elements:
        r = {}
        print "foo"

        #stop_id
        stop_id = stop.xpath('kml:name', namespaces=namespaces)[0].text
        r['id'] = stop_id

        stop_coords = stop.xpath('kml:Point/kml:coordinates')
        r['coords'] = stop_coords

        # change to description scope
        #stop = stop.xpath('kml:description/kml:table', namespaces=namespaces)

        stop_route = stop.xpath('kml:tr/kml:td[text()="Route"]/following-sibling::*', namespaces=namespaces)
        r['route'] = stop_route

        stop_street = stop.xpath('kml:tr/kml:td[text()="Street"]/following-sibling::*', namespaces=namespaces)
        r['street'] = stop_street
        stop_intersection = stop.xpath('kml:tr/kml:td[text()="Nearest Intersection"]/following-sibling::*', namespaces=namespaces)
        r['intersection'] = stop_intersection

        stop_elements_output.append(r)

    print stop_elements_output

    bus_elements = t.xpath('//kml:Placemark', namespaces=namespaces)
    bus_elements_output = []
    for bus_element in bus_elements:
        r = {}

        # Bus ID
        bus_id = bus_element.xpath('kml:name', namespaces=namespaces)[0].text

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
        r['next_stop'] = {'streets':next_stop}

        # Speed
        speed = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[text()="Speed"]/following-sibling::*', namespaces=namespaces)[0].text
        speed = speed.split()[0]
        r['speed'] = speed

        msg_time = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[text()="Msg Time"]/following-sibling::*', namespaces=namespaces)[0].text
        r['msg_time'] = msg_time

        r['bus_id'] = bus_id
        r['speed'] = speed
        bus_elements_output.append(r)
    return json.dumps(bus_elements_output)

application = bottle.default_app()


if __name__ == '__main__':
#    import pprint
#    pprint.pprint(go())
    from bottle import run
    debug(True)
    run(reloader=True)
