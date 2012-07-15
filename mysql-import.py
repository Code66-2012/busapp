#!/usr/bin/env python

import json

import MySQLdb
import memcache

import go


if __name__ == '__main__':
    conn = MySQLdb.connect('localhost', user='root', db='code66')
    cur = conn.cursor()

    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    data = go.go(go.live())

    mc.set('latest', json.dumps(data))

    for row in data:
        row['lat'] = row['coords']['lat']
        row['lon'] = row['coords']['lon']
        q = """insert into locations (
                    date,
                    date_w3cdtf,
                    routeID,
                    busID,
                    lat,
                    lon,
                    speed,
                    heading
                ) values (
                    '%(msg_time)s',
                    '%(msg_time)s',
                    %(route_id)s,
                    %(bus_id)s,
                    %(lat)s,
                    %(lon)s,
                    %(speed)s,
                    %(heading)s)""" % row
        #print q
        cur.execute(q)
        conn.commit()

    cur.close()
    conn.close()
