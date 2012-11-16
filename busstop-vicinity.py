#!/usr/bin/env python

import json

import MySQLdb
import memcache

import go

def locate(busses):
	conn = MySQLdb.connect('localhost', user='root', db='code66')
	cur = conn.cursor()
	mc = memcache.Client(['127.0.0.1:11211'], debug=0)	
	
	for bus in busses:
		if bus['next_stop']['tripID'] != 0:
			mc.set(str(bus['next_stop']['tripID']),0,20 * 60)
		print bus['next_stop']['name']
		print bus['next_stop']['tripID']
		print bus['next_stop']['time']
		print bus['route_id']		


if __name__ == '__main__':
	data = go.go(go.live())
	locate(data)
