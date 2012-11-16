#!/usr/bin/env python

import json

import MySQLdb
import memcache

import go

def locate(busses):
	conn = MySQLdb.connect('localhost', user='root', db='code66')
	cur = conn.cursor()
	
	for bus in busses:
		print bus['next_stop']['name']
		print [int(x[0]) for x in bus['next_stop']['stopID']]
		print bus['next_stop']['time']
		print bus['route_id']		


if __name__ == '__main__':
	data = go.go(go.live())
	locate(data)
