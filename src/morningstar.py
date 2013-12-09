#  morningstar.py - retrieve data from Morningstar for SMF Extension
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
import csv, urllib2
import yahoo

def find_exchange(self, ticker):
    """Determine exchange ticker is traded on so we can query morningstar"""
    # query yahoo to determine which exchange our ticker is traded on
    exchange = yahoo.fetch_data(self, ticker, 54)
    if exchange == 'AMEX':
        exchange = 'XASE'
        return exchange
    elif exchange =='NasdaqNM':
        exchange = 'XNAS'
        return exchange
    elif exchange =='NYSE':
        exchange = 'XNYS'
        return exchange
    #catch errors
    else:
        return exchange
    
def query_morningstar(self, exchange, symbol, url_ending):
    """Query morningstar for the data we want"""
    #determine whether we want key ratios or financial & query Morningstar  
    if url_ending == '&region=usa&culture=en-US&cur=USD&order=desc':
        url = ('http://financials.morningstar.com/ajax/exportKR2CSV.html?'
               '&callback=?&t=%s:%s%s' % (exchange, symbol, url_ending))
    else:
        url = ('http://financials.morningstar.com/ajax/ReportProcess4CSV.html?'
               '&t=%s:%s%s' % (exchange, symbol, url_ending))
    req = urllib2.Request(url)
    #catch errors
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError as e:
        self.keyratio_flag[0] = '1'
        self.financial_flag[0] = '1'
        if hasattr(e, 'reason'):
            return e.reason
        elif hasattr(e,'code'):
            return 'Error', e.code
    #verify response csv isn't empty
    sniff = response.readline()
    if str(sniff) == '':
        self.keyratio_flag[0] = '1'
        self.financial_flag[0] = '1'
        return 'Not Available'
    #discard first line if called by fetch_keyratios()
    if url_ending == '&region=usa&culture=en-US&cur=USD&order=desc':
        response.readline()
    return csv.reader(response)

def fetch_keyratios(self, ticker, datacode):
    """Get morningstar key ratio data and return desired element to user """
    #check for sane user input for datacode
    if datacode < 1 or datacode > 946:
        return 'Invalid Datacode'
    #check whether flags indicate that we already have the data we need
    if self.keyratio_flag[0] == '1' or self.keyratio_flag[1] != ticker:
        #query yahoo for exchange and check for errors
        exchange = find_exchange(self, ticker)
        if exchange not in ['XNYS', 'XASE', 'XNAS']:
            return exchange
        #query morningstar for key ratios and check for errors
        url_ending = '&region=usa&culture=en-US&cur=USD&order=desc'
        self.keyratio_reader = query_morningstar(self, exchange, ticker, 
                                                 url_ending)
        if self.keyratio_flag[0] == '1':
            return self.keyratio_reader
        #Set flags and read data into memory upon successful query
        else:
            self.keyratio_flag[0] = '0'
            self.keyratio_flag[1] = ticker
            self.keyratio_data = [row for row in self.keyratio_reader]
    #check for existing datacode -> value map, if none exists then create it
    if not hasattr(self, 'key_datacode_map'):
        self.key_datacode_map = keyratio_datacode_map()
    #lookup and return value from map
    row, col = self.key_datacode_map[datacode]
    return self.keyratio_data[row][col]

def keyratio_datacode_map():
    """ Create dictionary mapping datacodes to (row, col) in data. """
    # define rows that have no useful data
    skip_list = {16, 17, 18, 28, 29, 38, 39, 40, 41, 46, 51, 56, 61, 62, 63, 69,
                 70, 71, 92, 93, 98, 99, 100}
    def find_row_col(datacode):
        skipped = 0
        # match datacode to row, column
        for row in xrange(0, 109):
            if row in skip_list:
                skipped += 11
                continue
            for col in xrange(0, 12):
                if datacode == col + (11*row) - skipped:
                    return row, col
    # create and return the dictionary
    return {datacode: find_row_col(datacode) for datacode in xrange(1, 947)}

#TODO: Update getMorningFin to recycle local data like getMorningKey
def fetch_financials(self, ticker, datacode):
    """Get morningstar financial data and return desired element to user """
    if datacode < 1 or datacode > 162 :
        return 'Invalid Datacode'
    #check whether flags indicate that we already have the data we need
    if self.financial_flag[0] == '1' or self.financial_flag[1] != ticker:
        #query yahoo for exchange and check for errors
        exchange = find_exchange(self,ticker)
        if exchange not in ['XNYS', 'XASE', 'XNAS']:
            return exchange
        #query morningstar for financials and check for errors
        url_ending = ('&region=usa&culture=en-US&cur=USD&reportType=is'
                      '&period=12&dataType=A&order=desc&columnYear=5&rounding=3'
                      '&view=raw&r=113199&denominatorView=raw&number=3')
        financial_reader = query_morningstar(self, exchange, ticker, url_ending)
        if self.financial_flag[0] == '1':
            return financial_reader
        #Set flags and read data into memory upon successful query
        else:
            self.financial_flag[0] = '0'
            self.financial_flag[1] = ticker
            financial_data_setup(self, financial_reader)
    #check for existing datacode -> value map, if none exists then create it
    if not hasattr(self, 'fin_datacode_map'):
        self.fin_datacode_map = financial_datacode_map()
    #lookup and return value from map
    row, col = self.fin_datacode_map[datacode]
    return self.financial_data[row][col]

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
            try:
                if i[1] == 'TTM' and ttm_count == 0:
                    self.financial_data.append(i)
                    ttm_count = 1
                    continue
            #Skip appending Morningstar categories ie: 'Costs and expenses'
            except:
                continue   
            if i[0] == d:
                self.financial_data.append(i)
            elif d not in rfd_header:
                rfd_header.append(d)
                self.financial_data.append(['No Data', 'N/A', 'N/A', 'N/A',
                                            'N/A', 'N/A','N/A'])
    
def financial_datacode_map():
    """ Create dictionary mapping datacodes to (row, col) in data. """
    def find_row_col(datacode):
        #Match datacode to row, column.
        for row in xrange(0, 27):
            for col in xrange(0, 7):
                if datacode == col + (6*row):
                    return row, col
    #Create and return the dictionary.
    return {datacode: find_row_col(datacode) for datacode in xrange(1, 163)}