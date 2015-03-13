#  morningstar.py - Retrieve data from Morningstar for the SMF Extension
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
import csv
from urllib.request import Request, urlopen
from urllib.error import URLError
from codecs import iterdecode

def find_exchange(self, ticker):
    """Determine exchange ticker is traded on so we can query Morningstar"""
    exch_name = ['nasdaq','nyse','amex']
    #Get exchange lists we don't have already, and return ticker's exchange.
    for exch in exch_name:
        if exch == 'nasdaq':
            if self.exchange_flag[0] == '0':
                    query_nasdaq(self, exch)
                    self.exchange_flag[0] = '1'
            for i in self.nasdaq_list:                
                if ticker == i[0]:
                    return 'XNAS'
        if exch == 'nyse':
            if self.exchange_flag[1] == '0':
                    query_nasdaq(self, exch)
                    self.exchange_flag[1] = '1'
            for i in self.nyse_list:
                if ticker == i[0]:
                    return 'XNYS'
        if exch == 'amex':
            if self.exchange_flag[2] == '0':
                    query_nasdaq(self, exch)
                    self.exchange_flag[2] = '1'
            for i in self.amex_list:
                if ticker == i[0]:
                    return 'XASE'
    return 'Exchange lookup failed. Only NYSE, NASDAQ, and AMEX are supported.'

def query_nasdaq(self, exch_name):
    """Query Nasdaq for list of tickers by exchange"""
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
    url = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=%s&render=download' % (exch_name)
    req = Request(url, headers = header)
    try:
        response = urlopen(req)
    #Catch errors.
    except URLError as e:
        self.exchange_flag[0] = '1'
        if hasattr(e, 'reason'):
            return e.reason
        elif hasattr(e,'code'):
            return 'Error', e.code
    #Setup list(s) of exchange names.
    exch_result = csv.reader(iterdecode(response,'utf-8'))
    if exch_name == 'nasdaq':
        self.nasdaq_list = [row for row in exch_result]
    elif exch_name == 'nyse':
        self.nyse_list = [row for row in exch_result]
    elif exch_name == 'amex':
        self.amex_list = [row for row in exch_result]
    return 'Unknown Exception in query_nasdaq'
    
def query_morningstar(self, exchange, symbol, url_ending):
    """Query Morningstar for the data we want"""
    #Determine whether we want key ratios or financials & query Morningstar.  
    if url_ending == '&region=usa&culture=en-US&cur=USD&order=desc':
        url = ('http://financials.morningstar.com/ajax/exportKR2CSV.html?'
               '&callback=?&t=%s:%s%s' % (exchange, symbol, url_ending))
    else:
        url = ('http://financials.morningstar.com/ajax/ReportProcess4CSV.html?'
               '&t=%s:%s%s' % (exchange, symbol, url_ending))
    req = Request(url)
    #Catch errors.
    try:
        response = urlopen(req)
    except URLError as e:
        self.keyratio_flag[0] = '1'
        self.financial_flag[0] = '1'
        if hasattr(e, 'reason'):
            return e.reason
        elif hasattr(e,'code'):
            return 'Error', e.code
    #Verify response csv isn't empty.
    sniff = response.readline()
    if str(sniff) == '':
        self.keyratio_flag[0] = '1'
        self.financial_flag[0] = '1'
        return 'Not Available'
    #Discard first line if called by fetch_keyratios().
    if url_ending == '&region=usa&culture=en-US&cur=USD&order=desc':
        response.readline()
    return csv.reader(iterdecode(response,'utf-8'))

def fetch_keyratios(self, ticker, datacode):
    """Get Morningstar key ratio data and return desired element to user"""
    #Check for sane user input for datacode.
    if datacode < 1 or datacode > 946:
        return 'Invalid Datacode'
    #Check whether flags indicate that we already have the data we need.
    if self.keyratio_flag[0] == '1' or self.keyratio_flag[1] != ticker:
        #Query NASDAQ for exchange and check for errors.
        exchange = find_exchange(self, ticker)
        if exchange not in ['XNYS', 'XASE', 'XNAS']:
            return exchange
        #Query Morningstar for key ratios and check for errors.
        url_ending = '&region=usa&culture=en-US&cur=USD&order=desc'
        self.keyratio_reader = query_morningstar(self, exchange, ticker, 
                                                 url_ending)
        if self.keyratio_flag[0] == '1':
            return self.keyratio_reader
        #Set flags and read data into memory upon successful query.
        else:
            self.keyratio_flag[0] = '0'
            self.keyratio_flag[1] = ticker
            self.keyratio_data = [row for row in self.keyratio_reader]
            #Append day for ISO standard dates.
            for idx in range (2, 12):
                self.keyratio_data[0][idx] += '-01' 
    #Check for existing datacode -> value map, if none exists then create it.
    if not hasattr(self, 'key_datacode_map'):
        self.key_datacode_map = keyratio_datacode_map()
    #Lookup and return value from map.
    row, col = self.key_datacode_map[datacode]
    element = self.keyratio_data[row][col]
    #Strip , from str so we can convert to float
    return element.replace(',','')

def keyratio_datacode_map():
    """Create a dictionary mapping datacodes to (row, col) in data."""
    #Define rows that have no useful data.
    skip_list = {16, 17, 18, 28, 29, 38, 39, 40, 41, 46, 51, 56, 61, 62, 63, 69,
                 70, 71, 92, 93, 98, 99, 100}
    #Setup dictionary structure.
    allowed = sorted(set(range(109)) - skip_list)
    #Map datacode to row, column.
    def mapping (idx):
        row, col = divmod(idx - 1, 11)
        return allowed[row], col + 1
    #Create and return the dictionary.
    return {datacode: mapping(datacode) 
            for datacode in range(1, 947) }

def fetch_financials(self, fin_type, ticker, datacode):
    """Get Morningstar financial data and return desired element to user"""
    if datacode < 1 or datacode > 162:
        return 'Invalid Datacode'
    #Check whether flags indicate that we already have the data we need.
    flags = self.financial_flag
    if fin_type == 'qtr': 
        flags = self.qfinancial_flag   
    if flags[0] == '1' or flags[1] != ticker:
        #Query NASDAQ for exchange and check for errors.
        exchange = find_exchange(self,ticker)
        if exchange not in ['XNYS', 'XASE', 'XNAS']:
            return exchange
        #Query Morningstar for financials and check for errors.
        if fin_type == 'qtr':      
            url_ending = ('&region=usa&culture=en-US&cur=USD&reportType=is'
                      '&period=3&dataType=A&order=desc&columnYear=5&rounding=3'
                      '&view=raw&r=113199&denominatorView=raw&number=3')
        else:
            url_ending = ('&region=usa&culture=en-US&cur=USD&reportType=is'
                      '&period=12&dataType=A&order=desc&columnYear=5&rounding=3'
                      '&view=raw&r=113199&denominatorView=raw&number=3')
        financial_reader = query_morningstar(self, exchange, ticker, url_ending)
        if flags[0] == '1':
            return financial_reader
        #Set flags and read data into memory upon successful query.
        else:
            flags[0] = '0'
            flags[1] = ticker
            financial_data_setup(self, financial_reader)
    #Check for existing datacode -> value map, if none exists then create it.
    if not hasattr(self, 'fin_datacode_map'):
        self.fin_datacode_map = financial_datacode_map()
    #Lookup and return value from map.
    row, col = self.fin_datacode_map[datacode]
    element = self.financial_data[row][col]
    #Strip , from str so we can convert to float
    return element.replace(',','')

def financial_data_setup(self, financial_reader):
    """Setup our own data structure since Morningstar csv format varies."""
    header_list = ['Revenue', 'Cost of revenue', 'Gross profit',
                   'Research and development', 'Sales, General and '
                   'administrative', 'Depreciation and amortization',
                   'Interest expense', 'Other operating expenses',
                   'Total costs and expenses', 'Total operating expenses',
                   'Operating income', 'Interest Expense',
                   'Other income (expense)', 'Income before taxes',
                   'Income before income taxes', 'Provision for income taxes',
                   'Net income from continuing operations', 
                   'Net income from discontinuing ops', 'Other', 'Net income',
                   'Net income available to common shareholders', 'Basic',
                   'Diluted', 'EBITDA']
    #For row in Morningstar csv, if row[0] is in our list add the row.
    #Otherwise add an empty row.
    self.financial_data = []
    raw_financial_data = [row for row in financial_reader]
    rfd_header = [h[0] for h in raw_financial_data]            
    ttm_count = 0
    for d in header_list:                
        for i in raw_financial_data:
            #Handle corner case of first row.
            try:
                if i[1] == 'TTM' and ttm_count == 0:
                    self.financial_data.append(i)
                    ttm_count = 1
                    continue
            #Skip appending Morningstar categories ie: 'Costs and expenses'.
            except:
                continue   
            #Append our data and placeholder rows
            if i[0] == d:
                self.financial_data.append(i)
            elif d not in rfd_header:
                rfd_header.append(d)
                self.financial_data.append(['No Data', 'N/A', 'N/A', 'N/A',
                                            'N/A', 'N/A','N/A'])
    #Append day for ISO standard dates.
    for idx in range (2, 7):
        self.financial_data[0][idx] += '-01' 

def financial_datacode_map():
    """Create a dictionary mapping datacodes to (row, col) in data."""
    def mapping( idx ):
        row, col = divmod(idx - 1, 6)
        return row, col + 1
    return {idx: mapping(idx) for idx in range(1, 163)}