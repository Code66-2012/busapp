#!/usr/bin/env python

import bottle
import memcache

from bottle import response, route

mc = memcache.Client(['127.0.0.1:11211'], debug=0)

@route('/')
def get():
    response.content_type = 'application/json; charset=utf-8'
    response.set_header('Access-Control-Allow-Origin', '*')
    return mc.get('latest')

# For running within a WSGI container
application = bottle.default_app()

if __name__ == '__main__':
    from bottle import run
    run(reloader=True)
