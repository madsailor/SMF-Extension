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
#NOTE: Due to the way the site is structured, data is gathered for
#      1yr with the 1st call and in 5yr increments thereafter, for
#      a maximum of 21yrs total. The current implementation requests
#      pages in order from newest to oldest. Efficiency may be
#      increased by requesting only pages with needed data.
try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError
    from html.parser import HTMLParser
    major_version = 3
except ImportError:
    from urllib2 import Request, urlopen, URLError
    from HTMLParser import HTMLParser
    major_version = 2
import smf

def fetch_advfn(self, ticker, datacode):
    """Get ADVFN data and return desired element to user """
    if datacode < 1 or datacode > 5291 :
        return 'Invalid Datacode'
    if self.advfn_flag[3] == ticker and self.advfn_flag[5] == True:
        row, col = divmod(datacode - 1, len(self.total_advfn_data[0]))
        return self.total_advfn_data[row][col]
        
    if self.advfn_flag[3] != ticker or (datacode % 21) not in\
    range(self.advfn_flag[2]):
        query_advfn(self, ticker)#Enable for normal use.
#        test_query_advfn(self, ticker)#Enable for testing purposes only.
        if self.advfn_flag[4] != None:
            return self.advfn_flag[4]
        clean_advfn(self)
        organize_advfn(self)
    row, col = divmod(datacode - 1, len(self.total_advfn_data[0]))
    return self.total_advfn_data[row][col]

def test_query_advfn(self, ticker):
    """Open local html files for testing purposes"""
    import os
    working_dir = os.path.dirname(__file__)
    rel_path = "advfn/dd/"
    file_path = os.path.join(working_dir, rel_path)
    file = (file_path + str(self.advfn_start_list[self.advfn_flag[0]]) +'.html')
    try:
        with open(file,'r') as raw_advfn:
            #Parse raw html for the data we want and set flags on completion.
            parse_advfn = ADVFNParser()
            parse_advfn.feed(raw_advfn.read())
            self.advfn_data = parse_advfn.result()
            self.advfn_flag[0] += 1
            self.advfn_flag[3] = ticker
    except IOError as e:
        if hasattr(e, 'reason'):
            self.advfn_flag[4] = e.reason
        elif hasattr(e,'code'):
            self.advfn_flag[4] = e.code
        return 

def query_advfn(self, ticker):
    """Query ADVFN for the data we want"""
    exchange = advfn_exchange(self, ticker)
    if exchange not in ['NYSE', 'NASDAQ', 'AMEX']:
        return exchange
    url = 'http://www.advfn.com/stock-market/%s/%s/financials?btn=start_date&'\
          'start_date=%s&mode=annual_reports'%(exchange, ticker,
                                               self.advfn_start_list
                                               [self.advfn_flag[0]])
    req = Request(url)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            self.advfn_flag[4] = e.reason
        elif hasattr(e,'code'):
            self.advfn_flag[4] = e.code
        return 
    #Parse raw html for the data we want and set flags on completion.
    parse_advfn = ADVFNParser()
    if major_version == 3:
        r_html = response.read().decode(response.headers.get_content_charset())
    else:
        r_html = response.read().decode(response.headers.getparam('charset'))
    parse_advfn.feed(r_html)
    self.advfn_data = parse_advfn.result()
    self.advfn_flag[0] += 1
    self.advfn_flag[3] = ticker
    return

def clean_advfn(self):
    """Format raw html to useable data"""
    page = self.advfn_data
    self.advfn_flag[1] = 0
    #Strip month from year end date.
    for ye_idx in range(1,6):
        if len(page[ye_idx]) == 7:
            #Track year count for this dataset.
            self.advfn_flag[1] += 1
            ye_date = page[ye_idx]
            page[ye_idx]= ye_date[:4]
    #Strip commas (try/except for Python 2.x compatibility).
    for idx in range(len(page)):
        try:
            page[idx] = (str(page[idx])).translate({ord(i):None for i in ','})
        except:
            page[idx] = (str(page[idx])).translate(None, ',')
    #Strip non-numeric values (ie. data descriptors).
    for element in page[:]:
        if not is_number(element):
            page.remove(element)
    #Increment total year count for data we have already.
    self.advfn_flag[2] += self.advfn_flag[1]
    return

def organize_advfn(self):
    """Organize data into a 2d list"""
    organized_data = [self.advfn_data[idx:idx+self.advfn_flag[1]] for idx in
                      range(0,len(self.advfn_data), self.advfn_flag[1])]
    #Move newest years from last to first in array.
    [i.reverse() for i in organized_data]
    #Append 1st year data to our total data.
    if self.advfn_flag[0] == 1:
        self.old_advfn_data = organized_data
        self.total_advfn_data = organized_data
        return
    #Check for > 5yr chunk and pad missing elements.
    if (self.advfn_flag[1] > 1 and self.advfn_flag[1] < 5):
        while len(self.total_advfn_data[0]) < 21:
            [n.append('No Data')for n in self.total_advfn_data]                
        self.advfn_flag[5] = True
        return
    #Discard data we already have and pad missing elements.
    match = [i in self.total_advfn_data[0] for i in organized_data[0]]
    if True in match:
        while len(self.total_advfn_data[0]) < 21:
            [n.append('No Data')for n in self.total_advfn_data]                
        self.advfn_flag[5] = True
        return
    #Collate new data with total data.
    else:
        self.total_advfn_data = [x+y for x,y in zip(self.old_advfn_data,
                                                     organized_data)] 
        self.old_advfn_data = self.total_advfn_data
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