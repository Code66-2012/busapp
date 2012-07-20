#!/usr/bin/env python3

import json

import requests


lats = set()
lngs = set()

#with open('abq.json') as fp:
with requests.session() as s:
    fp = s.get('http://www.overpass-api.de/api/interpreter?data=[out:json];relation[name=Albuquerque];way%28r%29;node%28w%29;out;')
    j = fp.json
    for e in j['elements']:
        lats.add(e['lat'])
        lngs.add(e['lon'])

r = {}
r['maxlat'], r['maxlng'] = max(lats), max(lngs)
r['minlat'], r['minlng'] = min(lats), min(lngs)

bbox = [r['minlng'], r['minlat'], r['maxlng'], r['maxlat']]

print(r)
print()
print('# GeoJSON bbox: [minlng, minlat, maxlng, maxlat]')
print('bbox = {0}'.format(bbox))
