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
import MySQLdb
import memcache

import logging


def utf8_encode_callback(m):
    return unicode(m).encode()

def fix_latin1_mangled_with_utf8_maybe_hopefully_most_of_the_time(s):
    return re.sub('#[\\xA1-\\xFF](?![\\x80-\\xBF]{2,})#', utf8_encode_callback, s)


headers = {'user-agent': 'Code 66 hackathon'}
namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}

# create persistent session, so we don't hammer ABQ's servers too much
session = requests.session()
session.headers = headers


@route('/')
@route('/nyan') # backward compatibility, remove this
def returnJson():
    response.content_type = 'application/json'
    return json.dumps(go(live()))

def live():

    d = session.get('http://data.cabq.gov/transit/realtime/route/allroutes.kml')
    raw_document = d.content

    return raw_document

def get_stops():
    session = requests.session()
    session.headers = headers

    stops = session.get('http://data.cabq.gov/transit/routesandstops/transitstops.kmz')
    raw_stops = stops.content

    raw_stops = zipfile.ZipFile(StringIO(raw_stops), 'r')
    raw_stops = raw_stops.open('doc.kml').read()
    raw_stops = raw_stops.decode('utf-8')
    raw_stops = raw_stops.replace('http://earth.google.com/kml/2.2', namespaces['kml'])
    raw_stops = raw_stops.replace('<![CDATA[', '')
    raw_stops = raw_stops.replace(']]>', '')
    raw_stops = raw_stops.encode('utf-8')
    

    st = etree.fromstring(raw_stops)
    stop_elements = st.xpath('//kml:Placemark', namespaces=namespaces)
    stop_elements_output = []
    for stop in stop_elements:
        r = {}

        #stop_id
        #stop_routes = stop.xpath('kml:name', namespaces=namespaces)[0].text
        #r['routes'] = stop_routes

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
        #stop_name = stop.xpath('kml:description//kml:table/kml:tr/kml:td[text()="Name"]/following-sibling::*', namespaces=namespaces)[0].text
        #r['name'] = stop_name
        stop_street = stop.xpath('kml:description//kml:table/kml:tr/kml:td[text()="Street"]/following-sibling::*', namespaces=namespaces)[0].text
        #r['street'] = stop_street
        #print stop_street
        stop_intersection = stop.xpath('kml:description//kml:table/kml:tr/kml:td[text()="Nearest Intersection"]/following-sibling::*', namespaces=namespaces)[0].text
        #r['intersection'] = stop_intersection
        #stop_serves = stop.xpath('kml:description//kml:table/kml:tr/kml:td[text()="Serving"]/following-sibling::*', namespaces=namespaces)[0].text
        #r['serves'] = stop_serves
        r['name'] = """%s , %s""" % (stop_street, stop_intersection)
        stop_direction = stop.xpath('kml:description//kml:table/kml:tr/kml:td[text()="Direction"]/following-sibling::*', namespaces=namespaces)[0].text
        r['direction'] = stop_direction

        stop_elements_output.append(r)

    return stop_elements_output




def get_trip_id(street, time, route):
    #mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    conn = MySQLdb.connect('localhost', 'app', '6,$S{1MOL$6_"5lft6',charset='utf8')
    cur = conn.cursor()

    if not street:
        return
    #stops = mc.get('latest')
    dotw = datetime.datetime.utcnow() + datetime.timedelta(hours = -9)
    dotw = dotw.weekday()
    schedule = "wkd"
    if dotw == 6:
        schedule = "sun"
    if dotw == 5:
        schedule = "sat"

    q = u"SELECT DISTINCT trip_id FROM `abqride`.`trip_map` WHERE `active_"+schedule+"` = 1 AND `arrival_time` LIKE %s AND `route` =%s AND stop_code IN (SELECT stop_code FROM abqride.stops WHERE stop_name = %s) "
    cur.execute(q, (time+'%',route,street))
    
    tripID = [int(x[0]) for x in cur.fetchall()]
    
    if len(tripID) == 1:
        return tripID[0]
    else:
        return 0

def go(raw_document):

    raw_document = raw_document.decode('iso-8859-1')
    raw_document = raw_document.encode('utf-8')
    #raw_document = fix_latin1_mangled_with_utf8_maybe_hopefully_most_of_the_time(raw_document)

    t = etree.fromstring(raw_document)
    
    bus_elements = t.xpath('//kml:Placemark', namespaces=namespaces)
    bus_elements_output = []
    for bus_element in bus_elements:
        r = {}

        # Bus ////////////////////ID
        bus_id = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[text()="Vehicle #"]/following-sibling::*', namespaces=namespaces)[0].text
        r['bus_id'] = int(bus_id)

        # Route ID
        route_id = bus_element.xpath('kml:name', namespaces=namespaces)
        if not route_id:
            continue
        route_id = route_id[0].text
        if route_id == 'Off Duty':
            continue
        r['route_id'] = int(route_id)

        # Coordinates
        coords = bus_element.xpath('kml:Point/kml:coordinates', namespaces=namespaces)[0].text
        coords = coords.split(',')
        coords_out = {}
        coords_out['lon'] = float(coords[0])
        coords_out['lat'] = float(coords[1])
        r['coords'] = coords_out

        # Next Stop
        next_stop = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[normalize-space(text())="Next Stop"]/following-sibling::*', namespaces=namespaces)
        if not next_stop:
            next_stop = bus_element.xpath('kml:description/kml:table/kml:tr/kml:td[normalize-space(text())="Deadhead"]/following-sibling::*', namespaces=namespaces)
        if not next_stop:
            # how and why did we get here? bus is operating, but no next stop?
            logging.warn("No next stop?")
            continue
        next_stop = next_stop[0].text
        next_stop_match = re.match('(Next stop is )?(.+) @ (\d\d?:\d\d\s[AP]M)', next_stop)
        if next_stop_match:
            next_stop = next_stop_match.groups()
            next_stop_name = next_stop[1]
            scheduled_time = time.strptime(next_stop[2],'%I:%M %p')
            stop_time = time.strftime('%H:%M',scheduled_time)
            next_stop_id = get_trip_id(next_stop_name,stop_time,r['route_id'])
            r['next_stop'] = {'tripID': next_stop_id, 'name':next_stop_name, 'time':stop_time}
        else:
            #logging.warn("No match for "+next_stop)
            continue
        
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
        time_diff_secs = time.mktime(time.strptime(r['msg_time_raw'],'%I:%M:%S %p')) - time.mktime(scheduled_time)
        if time_diff_secs > 0:
            r['time_diff'] =  time_diff_secs
        elif time_diff_secs < -60:
            r['time_diff'] = time_diff_secs
        else:
            r['time_diff'] =  0
        r['msg_time'] = msg_time.isoformat()
        r['msg_time_epoch'] = time.mktime(msg_time.timetuple())

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
