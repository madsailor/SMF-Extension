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
import sys
import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError
from codecs import iterdecode

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
            self.yahoo_data = [row for row in self.yahoo_reader]
            cleanup_yahoo(self)
    return self.yahoo_data[0][int(datacode)-1]

def cleanup_yahoo(self):
    """Cleanup as many elements as possible to standardized forms"""
    #Format dividend dates to ISO standard.
    cleanup_divdate(self)
    #Format last trade date to ISO standard.
    self.yahoo_data[0][9] = str((datetime.datetime.strptime(self.yahoo_data[0][9],'%m/%d/%Y')).date())
    #Format last trade time to ISO standard.
    self.yahoo_data[0][13] = str((datetime.datetime.strptime(self.yahoo_data[0][13],'%I:%M%p')).time())
    #Strip % from chg in pct, moving avg's, and pct chg from 52wk high/low.
    for index_1 in (15, 19, 23, 47, 49):
        self.yahoo_data[0][index_1] = (self.yahoo_data[0][index_1]).translate({ord(i):None for i in '%'})
    #Convert market cap, rev, EBITDA to floats.
    for index_2 in (43, 70, 72):
        big_val = self.yahoo_data[0][index_2]
        if 'B' in big_val:
            self.yahoo_data[0][index_2] = ((float(big_val.translate({ord(i):None for i in 'B'})))*1000000000)
        elif 'M' in big_val:
            self.yahoo_data[0][index_2] = ((float(big_val.translate({ord(i):None for i in 'M'})))*1000000)
    return

def cleanup_divdate(self):
    """Change dividend dates to ISO standard format"""
    ip_date = self.yahoo_data[0][3]
    ie_date = self.yahoo_data[0][5]
    #Add current year to dates. 
    cur_date = datetime.date.today()
    ip_date += '{0:>5}'
    ie_date += '{0:>5}'
    #Format to ISO standard.
    revp_date = ((datetime.datetime.strptime(ip_date.format(cur_date.year), '%b %d %Y'))).date() 
    reve_date = ((datetime.datetime.strptime(ie_date.format(cur_date.year), '%b %d %Y'))).date()
    #Increment year of ex and pay dates if pay date is in the past.
    if cur_date > revp_date:
        revp_date = revp_date + datetime.timedelta(days=365)
        reve_date = reve_date + datetime.timedelta(days=365)
    #Decrement year of ex date if it's after pay date
    if reve_date > revp_date:
        reve_date = reve_date - datetime.timedelta(days=365)
    self.yahoo_data[0][3] = (str(revp_date))
    self.yahoo_data[0][5] = (str(reve_date))
    return

def query_yahoo(self, ticker, stat):
    """Query Yahoo for the data we want""" 
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (ticker, stat)
    req = Request(url)
    try:
        response = urlopen(req)
    #Catch errors.
    except URLError as e:
        self.yahoo_flag[0] = '1'
        if hasattr(e, 'reason'):
            return e.reason
        elif hasattr(e,'code'):
            return 'Error', e.code
    if sys.version_info.major == 3:
        return csv.reader(iterdecode(response,'utf-8'))
    return csv.reader(response)   
