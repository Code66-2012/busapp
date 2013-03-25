#!/usr/bin/env python

import json

import MySQLdb
import memcache

import go

def locate(busses):
	#conn = MySQLdb.connect('localhost', user='root', db='code66')
	#cur = conn.cursor()
	mc = memcache.Client(['127.0.0.1:11211'], debug=0)	
        count = 0
        mc.set('latest', json.dumps(busses))	

	for bus in busses:
		if bus['next_stop']['tripID'] != 0:
			mc.set(str(bus['next_stop']['tripID']),str(bus['time_diff']),10 * 60)
		        if bus['time_diff'] < 90:
                            count += 1
                        mc.set(str(bus['next_stop']['tripID'])+"_bus",str(bus['bus_id']),180*60)
                mc.set(str(bus['bus_id'])+"_ns",bus['next_stop']['name'],180*60)
                mc.set(str(bus['bus_id'])+"_coords",str(bus['coords']['lat'])+":"+str(bus['coords']['lon']),180*60)
                #print bus['next_stop']['name']
		#print str(bus['next_stop']['tripID']) + ":" + str(bus['time_diff']) + ":" + str(bus['bus_id'])	
		#print bus['route_id']		
        mc.set("on_time_percent",str(float(count)/len(busses)),60*10)

if __name__ == '__main__':
	data = go.go(go.live())
        locate(data)
