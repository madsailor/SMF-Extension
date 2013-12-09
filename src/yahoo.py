#  yahoo.py - Retrieve data from Yahoo Finance for the SMF Extension.
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
#  Inspired by ystockquote by Corey Goldberg (cgoldberg@gmail.com)
#
import csv
import urllib2

def fetch_data(self, ticker, datacode):
    """Get Yahoo data and return desired element to user"""
    #Check for sane user input for datacode.
    if datacode < 1 or datacode > 81 :
        return 'Invalid Datacode'
    #Setup list of Yahoo-defined elements to query with.
    query_list = ['y','d','b2','r1','b3','q','p','o','c1','d1','c','d2','c6',
                  't1','k2','p2','c8','m5','c3','m6','g','m7','h','m8','k1',
                  'm3','l','m4','l1','t8','w1','g1','w4','g3','p1','g4','m',
                  'g5','m2','g6','k','v','j','j1','j5','j3','k4','j6','n','k5',
                  'n4','w','s1','x','v','a5','b6','k3','t7','a2','t6','i5','l2',
                  'e','l3','e7','v1','e8','v7','e9','s6','b4','j4','p5','p6',
                  'r','r2','r5','r6','r7','s7']
    stat = ''.join(query_list)
    #Check whether flags indicate we already have the data we need.
    if self.yahoo_flag[0] == '1' or self.yahoo_flag[1] != ticker:
        self.yahoo_reader = query_yahoo(self, ticker, stat)
        #Catch errors.
        if self.yahoo_flag[0] == '1':
            return self.yahoo_reader
        #Set flags upon successful query.
        else:
            self.yahoo_flag[0] = '0'
            self.yahoo_flag[1] = ticker
            #Store csv in memory.
            for row in self.yahoo_reader:
                self.yahoo_data = row
    return self.yahoo_data[int(datacode)-1]

def query_yahoo(self, ticker, stat):
    """Query Yahoo for the data we want""" 
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (ticker, stat)
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
    #Catch errors.
    except urllib2.URLError as e:
        self.yahoo_flag[0] = '1'
        if hasattr(e, 'reason'):
            return e.reason
        elif hasattr(e,'code'):
            return 'Error', e.code
    return csv.reader(response)   