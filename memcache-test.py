#!/usr/bin/env python

import json

import memcache


if __name__ == '__main__':
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)

    print mc.get('latest')
