#!/usr/bin/env python

import json

import MySQLdb
import memcache

import go

def locate(busses):
	conn = MySQLdb.connect('localhost', user='root', db='code66')
	cur = conn.cursor()
	
	for bus in busses:
		print bus['next_stop']['streets']
		print bus['next_stop']['stopID']
		

if __name__ == '__main__':
	data = go.go(go.live())
	locate(data)