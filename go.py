#!/usr/bin/env python
# vim: ts=4 sw=4 et

from __future__ import unicode_literals

import argparse
import datetime
import json
import time
import re

import dateutil.parser, dateutil.tz
import bottle
import requests

from bottle import route, debug, response
from lxml import etree
import re
import zipfile
from StringIO import StringIO


def utf8_encode_callback(m):
    return unicode(m).encode()

def fix_latin1_mangled_with_utf8_maybe_hopefully_most_of_the_time(s):
    return re.sub('#[\\xA1-\\xFF](?![\\x80-\\xBF]{2,})#', utf8_encode_callback, s)


headers = {'user-agent': 'Code 66 hackathon'}
namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}

# create persistent session, so we don't hammer ABQ's servers too much
session = requests.session(headers=headers)


@route('/')
@route('/nyan') # backward compatibility, remove this
def returnJson():
    response.content_type = 'application/json'
    return json.dumps(go(live()))

def live():

    d = session.get('http://data.cabq.gov/transit/realtime/introute/intallbuses.kml')
    raw_document = d.content

    return raw_document

def get_stops():
    session = requests.session(headers=headers)

    stops = session.get('http://data.cabq.gov/transit/routesandstops/transitstops.kmz')
    raw_stops = stops.content

    raw_stops = zipfile.ZipFile(StringIO(raw_stops), 'r')
    raw_stops = raw_stops.open('doc.kml').read()
    raw_stops = raw_stops.replace('http://earth.google.com/kml/2.2', namespaces['kml'])
    raw_stops = raw_stops.replace('<![CDATA[', '')
    raw_stops = raw_stops.replace(']]>', '')
    raw_stops = raw_stops.decode('iso-8859-1')
    raw_stops = raw_stops.encode('utf-8')

    st = etree.fromstring(raw_stops)
    stop_elements = st.xpath('//kml:Placemark', namespaces=namespaces)
    stop_elements_output = []
    for stop in stop_elements:
        r = {}

        #stop_id
        stop_routes = stop.xpath('kml:name', namespaces=namespaces)[0].text
        r['routes'] = stop_routes

        stop_coords = stop.xpath('kml:Point/kml:coordinates', namespaces=namespaces)[0].text
        stop_coords = stop_coords.split(',')
        coords_out = {}
        coords_out['lon'] = float(stop_coords[0])
        coords_out['lat'] = float(stop_coords[1])
        r['coords'] = coords_out

        # change to description scope
        #stop = stop.xpath('kml:description//kml:table', namespaces=namespaces)

        stop_id = stop.xpath('kml:description//kml:table/kml:tr/kml:td[text()="Stop ID"]/following-sibling::*', namespaces=namespaces)[0].text
        if stop_id == '0':
            continue
        r['id'] = stop_id

        stop_street = stop.xpath('kml:description//kml:table/kml:tr/kml:td[text()="Street"]/following-sibling::*', namespaces=namespaces)[0].text
        r['street'] = stop_street
        #print stop_street
        stop_intersection = stop.xpath('kml:description//kml:table/kml:tr/kml:td[text()="Nearest Intersection"]/following-sibling::*', namespaces=namespaces)[0].text
        r['intersection'] = stop_intersection

        stop_direction = stop.xpath('kml:description//kml:table/kml:tr/kml:td[text()="Direction"]/following-sibling::*', namespaces=namespaces)[0].text
        r['direction'] = stop_direction

        stop_elements_output.append(r)

    return stop_elements_output


def go(raw_document):

    raw_document = raw_document.decode('iso-8859-1')
    raw_document = raw_document.encode('utf-8')
    #raw_document = fix_latin1_mangled_with_utf8_maybe_hopefully_most_of_the_time(raw_document)

    t = etree.fromstring(raw_document)
    
    bus_elements = t.xpath('//kml:Placemark', namespaces=namespaces)
    bus_elements_output = []
    for bus_element in bus_elements:
        r = {}

        # Bus ID
        bus_id = bus_element.xpath('kml:name', namespaces=namespaces)[0].text
        r['bus_id'] = int(bus_id)

        # Route ID
        route_id = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[text()="Route"]/following-sibling::*', namespaces=namespaces)
        if not route_id:
            continue
        route_id = route_id[0].text
        if route_id == 'Off Duty':
            continue
        r['route_id'] = int(route_id)

        # Next Stop
        next_stop = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[normalize-space(text())="Next Stop"]/following-sibling::*', namespaces=namespaces)
        if not next_stop:
            next_stop = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[normalize-space(text())="Deadhead"]/following-sibling::*', namespaces=namespaces)
        next_stop = next_stop[0].text
        next_stop = re.match('(Next stop is )?(.*) @(.*) scheduled', next_stop)
        if next_stop:
            next_stop = next_stop.groups()
            next_stop = next_stop[-2:]
            next_stop = [i.strip() for i in next_stop]
        next_stop_id = get_stop_id(next_stop, stop_elements_output)
        r['next_stop'] = {'streets':next_stop}

        # Speed
        speed = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[text()="Speed"]/following-sibling::*', namespaces=namespaces)[0].text
        speed = speed.split()[0]
        r['speed'] = float(speed)

        # Message Time
        msg_time = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[text()="Msg Time"]/following-sibling::*', namespaces=namespaces)[0].text
        r['msg_time_raw'] = msg_time
        # bug here: need to make sure for times the previous night, we're not setting date in the future
        now = datetime.datetime.now(tz=dateutil.tz.gettz('US/Mountain'))
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        msg_time = dateutil.parser.parse(msg_time, default=now)
        r['msg_time'] = msg_time.isoformat()
        r['msg_time_epoch'] = time.mktime(msg_time.timetuple())

        # Coordinates
        coords = bus_element.xpath('kml:Point/kml:coordinates', namespaces=namespaces)[0].text
        coords = coords.split(',')
        coords_out = {}
        coords_out['lon'] = float(coords[0])
        coords_out['lat'] = float(coords[1])
        r['coords'] = coords_out

        # Heading
        heading = bus_element.xpath('kml:Style/kml:IconStyle/kml:heading', namespaces=namespaces)[0].text
        r['heading'] = int(heading)

        bus_elements_output.append(r)
    return bus_elements_output

application = bottle.default_app()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make real-time data about Albuquerque buses less stupid')
    parser.add_argument('--filename', '-i', help='Offline KML file to parse')
    parser.add_argument('--live', action='store_true', default=False, help='Fetch live data from ABQdata')

    args = parser.parse_args()

    # fetch data live
    if args.live:
        import pprint
        pprint.pprint(go(live()))
    # if we've a filename, process it and quit
    elif args.filename:
        import pprint

        with open(args.filename) as fp:
            data = fp.read()
            pprint.pprint(go(data))
    # if no filename, start Web server for live querying
    else:
        from bottle import run
        debug(True)
        run(reloader=True)
