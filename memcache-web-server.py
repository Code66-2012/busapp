#!/usr/bin/env python

import memcache

from bottle import response, route

@route('/')
def get():
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    response.content_type = 'application/json; charset=utf-8'
    response.set_header('Access-Control-Allow-Origin', '*')
    return mc.get('latest')

if __name__ == '__main__':
    from bottle import run
    run(reloader=True)
