#!/usr/bin/env python

from __future__ import unicode_literals

import codecs
import requests
from lxml import etree

headers = {'user-agent': 'Code 66 hackathon'}
namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}

def go():
    session = requests.session(headers=headers)

    d = session.get('http://data.cabq.gov/transit/realtime/introute/intallbuses.kml')
    raw_document = d.content
    print 'raw document length:', len(raw_document)

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

        # Route ID
        route_id = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[text()="Route"]/following-sibling::*', namespaces=namespaces)
        if not route_id:
            continue
        route_id = route_id[0].text
        if route_id == 'Off Duty':
            continue
        r['route_id'] = route_id

        # Speed
        speed = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[text()="Speed"]/following-sibling::*', namespaces=namespaces)[0].text
        speed = speed.split()[0]
        r['speed'] = speed

        msg_time = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[text()="Msg Time"]/following-sibling::*', namespaces=namespaces)[0].text
        r['msg_time'] = msg_time

        r['bus_id'] = bus_id
        r['speed'] = speed
        bus_elements_output.append(r)
    return bus_elements_output

if __name__ == '__main__':
    import pprint
    pprint.pprint(go())
