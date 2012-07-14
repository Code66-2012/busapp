#!/usr/bin/env python
# vim: ts=4 sw=4 et

from __future__ import unicode_literals

import datetime
import json
import re

import dateutil.parser, dateutil.tz
import bottle
import requests

from bottle import route, debug, response
from lxml import etree

def utf8_encode_callback(m):
    return unicode(m).encode()

def fix_latin1_mangled_with_utf8_maybe_hopefully_most_of_the_time(s):
    return re.sub('#[\\xA1-\\xFF](?![\\x80-\\xBF]{2,})#', utf8_encode_callback, s)

headers = {'user-agent': 'Code 66 hackathon'}
namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}

@route('/')
@route('/nyan') # backward compatibility, remove this
def returnJson():
    return json.dumps(go())

def go():
    response.content_type = 'application/json'

    session = requests.session(headers=headers)

    d = session.get('http://data.cabq.gov/transit/realtime/introute/intallbuses.kml')
    stops = session.get('http://data.cabq.gov/transit/routesandstops/transitstops.kmz')
    raw_document = d.content

    #raw_document = file('tests/intallbuses.kml').read()

    raw_document = raw_document.decode('latin1')
    raw_document = raw_document.encode('utf-8', 'xmlcharrefreplace')
    raw_document = fix_latin1_mangled_with_utf8_maybe_hopefully_most_of_the_time(raw_document)

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
        else:
            print next_stop
        r['next_stop'] = next_stop

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
#    import pprint
#    pprint.pprint(go())
    from bottle import run
    debug(True)
    run(reloader=True)
