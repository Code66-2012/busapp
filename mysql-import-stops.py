#!/usr/bin/env python

import json

import MySQLdb
import memcache

import go

if __name__ == '__main__':
    conn = MySQLdb.connect('localhost', user='dev', passwd='root', db='code66')
    cur = conn.cursor()

    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    data = go.get_stops()

    #print json.dumps(data)
    mc.set('stops', json.dumps(data))

    for row in data:
        q_exists = """SELECT stopID FROM stops WHERE stopID = '%s'""" % row['id']
        if cur.execute(q_exists) > 0:
            continue
        row['lat'] = row['coords']['lat']
        row['lon'] = row['coords']['lon']
        q = """insert into stops (
                    stopID,
                    routes,
                    lat,
                    lon,
                    street,
                    intersection,
                    direction
                ) values (
                    %(id)s,
                    '%(routes)s',
                    %(lat)s,
                    %(lon)s,
                    '%(street)s',
                    '%(intersection)s',
                    '%(direction)s')
                """ % row
        #print q
        cur.execute(q)
        conn.commit()

    cur.close()
    conn.close()


