#  yahoo.py - retrieve data from Yahoo Finance for SMF Extension
#
#  Copyright (c) 2013 David Capron (drbluesman@yahoo.com)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  Based on ystockquote by Corey Goldberg (cgoldberg@gmail.com)
#
#from urllib2 import Request, urlopen
import urllib2

def fetch_data(symbol, datacode):
    if datacode < 1 or datacode > 83 :
        return 'Invalid Datacode'
    query_list = ['y','d','b2','r1','b3','q','p','o','c1','d1','c','d2','c6','t1','k2','p2','c8','m5','c3','m6','g','m7','h','m8','k1','m3','l','m4','l1','t8','w1','g1','w4','g3','p1','g4','m','g5','m2','g6','k','v','j','j1','j5','j3','k4','f6','j6','n','k5','n4','w','s1','x','j2','v','a5','b6','k3','t7','a2','t6','15','l2','e','l3','e7','v1','e8','v7','e9','s6','b4','j4','p5','p6','r','r2','r5','r6','r7','s7']
    for val in range(0, len(query_list)):
        if val == datacode - 1: 
            stat = query_list[val]
    #query remote and catch error
    return query_yahoo(symbol, stat)

def query_yahoo(symbol, stat): 
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            return e.reason
        elif hasattr(e,'code'):
            return 'Error', e.code
    return str(response.read().decode('utf-8').strip())
