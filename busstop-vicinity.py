#!/usr/bin/env python

import json

import MySQLdb
import memcache

import go

def locate(busses):
    #conn = MySQLdb.connect('localhost', user='root', db='code66')
    #cur = conn.cursor()
    mc = memcache.Client(['127.0.0.1:11211'])	
    count = 0
    mc.set('latest', json.dumps(busses))	

    for bus in busses:
        if bus['next_stop']['tripID'] != 0:
            if bus['time_diff'] < 90:
                count += 1 #counting late busses
            mc.set(str(bus['next_stop']['tripID'])+"_bus",str(bus['bus_id']),180*60) #set a bus id for this trip
            mc.set(str(bus['bus_id']),str(bus['next_stop']['tripID']),30*60) #set a trip for this bus
        elif mc.get(str(bus['bus_id'])): #if no trip id was determined, use the last one for this bus 
            bus['next_stop']['tripID'] = mc.get(str(bus['bus_id']))
        else:
            print ("No trip ID, hopefully starting a new trip")
        if mc.get(str(bus['bus_id'])+"_ns") != bus['next_stop']['name'] and bus['next_stop']['tripID'] != 0: # if new next stop
            print ("just passed or left a stop")
            mc.set(str(bus['next_stop']['tripID']),mc.get(str(bus['next_stop']['tripID'])+"_temp"),15 * 60) # use temporary lateness from last stop, now that stop has passed
        elif mc.get(str(bus['next_stop']['tripID'])) and float(mc.get(str(bus['next_stop']['tripID']))) < float(mc.get(str(bus['next_stop']['tripID'])+"_temp")):
            print ("later than previous")
            mc.set(str(bus['next_stop']['tripID']),mc.get(str(bus['next_stop']['tripID'])+"_temp"),15 * 60) # bus is already later to next stop than it was to previous
        mc.set(str(bus['next_stop']['tripID'])+"_temp",str(bus['time_diff']),10*60) #set how late this bus is to next stop
        mc.set(str(bus['bus_id'])+"_ns",bus['next_stop']['name'],180*60)
        mc.set(str(bus['bus_id'])+"_coords",str(bus['coords']['lat'])+":"+str(bus['coords']['lon']),180*60)
        print (str(bus['next_stop']['tripID']) + ":" + str(bus['time_diff']) + ":" + str(bus['bus_id']))
        #print bus['route_id']
    mc.set("on_time_percent",str(float(count)/len(busses)),60*10)
    
if __name__ == '__main__': 
    data = go.go(go.live())
    locate(data)
