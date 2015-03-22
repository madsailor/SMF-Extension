#  advfn.py - Retrieve data from ADVFN for the SMF Extension
#
#  Copyright (c) 2015 David Capron (drbluesman@yahoo.com)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError
except ImportError:
    from urllib2 import Request, urlopen, URLError
from html.parser import HTMLParser
import smf

def fetch_advfn(self, ticker, datacode):
    """Get ADVFN data and return desired element to user """
    if datacode < 1 or datacode > 252 :
        return 'Invalid Datacode'
#TODO: Map datacodes to alter start
    start = 0
    if self.advfn_flag[0] == 'Error' or self.advfn_flag[1] != ticker:
        if self.advfn_flag[0] == '1':
            return self.advfn_data
        query_advfn(self, ticker, start)#Enable for normal use.
#        test_query_advfn(self, ticker, start)#Enable for testing purposes only.
        clean_advfn(self)
    return self.advfn_data[datacode-1]

def test_query_advfn(self, ticker, start):
    """Open local html files for testing purposes"""
    with open((str(self.advfn_start[start]) +'.html'),'r') as raw_advfn:
        #Parse raw html for the data we want
        parse_advfn = ADVFNParser()
        parse_advfn.feed(raw_advfn.read())
        self.advfn_data = parse_advfn.result()
    self.advfn_flag[0] += self.advfn_start[start]
    self.advfn_flag[1] = ticker
    return 

def query_advfn(self, ticker, start):
    """Query ADVFN for the data we want"""
    exchange = advfn_exchange(self, ticker)
    if exchange not in ['NYSE', 'NASDAQ', 'AMEX']:
        return exchange
    url = 'http://www.advfn.com/stock-market/%s/%s/financials?btn=start_date&start_date=%s&mode=annual_reports' % (exchange, ticker, self.advfn_start[0])
    req = Request(url)
    try:
        response = urlopen(req)
        self.advfn_flag[0] += self.advfn_start[start]
        self.advfn_flag[1] = ticker
    except URLError as e:
        self.advfn_flag[0] = 'Error'
        if hasattr(e, 'reason'):
            return e.reason
        elif hasattr(e,'code'):
            return 'Error', e.code
    #Parse raw html for the data we want
    parse_advfn = ADVFNParser()
    raw_html = response.read().decode(response.headers.get_content_charset())
    parse_advfn.feed(raw_html)
    self.advfn_data = parse_advfn.result()
    return

def clean_advfn(self):
    """Format raw html to useable data"""
    #Keep track of how many years are in this dataset.
    year_count = 0
    page = self.advfn_data
    #Strip month from year end date.
    for ye_idx in range(1,6):
        if len(page[ye_idx]) == 7:
#TODO: Use yearcount with datacode mapping
            year_count += 1
            ye_date = page[ye_idx]
            page[ye_idx]= ye_date[:4]
    #Strip commas (try/except for Python 2.x compatibility)
    for idx in range(len(page)):
        try:
            page[idx] = (str(page[idx])).translate({ord(i):None for i in ','})
        except:
            page[idx] = (str(page[idx])).translate(None, ',')
    #Strip non-numeric values (ie. data descriptors).
    for element in page[:]:
        if not is_number(element):
            page.remove(element)
    return

def is_number(element):
    """Test for number vs. non-number strings"""
    try:
        float(element)
        return True
    except ValueError:
        return False

def advfn_exchange(self, ticker):
    """Determine exchange ticker is traded on so we can query advfn"""
    exchange = smf.find_exchange(self, ticker)    
    if exchange == 'XNAS':
        return 'NASDAQ'
    elif exchange == 'XNYS':
        return 'NYSE'
    elif exchange == 'XASE':
        return 'AMEX'
    return exchange
#TODO: Create this map.
def advfn_datacode_map(self, datacode):
    """Map datacodes to appropriate data elements."""
    return

class ADVFNParser(HTMLParser):
    """Class to parse ADVFN html. 'handle' methods are built-in"""
    def __init__(self):
        HTMLParser.__init__(self)
        self.data_list = []
        self.lasttag = None
        self.inLink = False
        
    def handle_starttag(self, tag, attrs):
        if tag == "td":
            for name, value in attrs:
                if name =="class" and (value == "s" or value == "sb"):
                    self.inLink = True
                    self.lasttag = tag
    
    def handle_endtag(self, tag):
        if tag == "td":
            self.inlink = False
        
    def handle_data(self, data):
        if self.lasttag == 'td' and self.inLink and data.strip():
            self.data_list.append(data)

    def result(self):
        return self.data_list