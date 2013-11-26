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

def find_exchange(ticker):
    """Determine exchange ticker is traded on so we can query morningstar"""
    # query yahoo to determine which exchange our ticker is traded on
    exchange = yahoo.fetch_data(ticker, 55)
    if exchange == '"AMEX"':
        exchange = 'XASE'
        return exchange
    elif exchange =='"NasdaqNM"':
        exchange = 'XNAS'
        return exchange
    elif exchange =='"NYSE"':
        exchange = 'XNYS'
        return exchange
    else:
        return exchange
    
def query_morningstar(self, exchange, symbol, url_ending):
    """Query morningstar for the data we want"""
    #determine whether we want key ratios or financial & query morningstar  
    if url_ending == '&region=usa&culture=en-US&cur=USD&order=desc':
        url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?&callback=?&t=%s:%s%s' % (exchange, symbol, url_ending)
    else:
        url = 'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?&t=%s:%s%s' % (exchange, symbol, url_ending)
    req = urllib2.Request(url)
    #catch errors
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError as e:
        self.flag[0] = '1'
        if hasattr(e, 'reason'):
            return e.reason
        elif hasattr(e,'code'):
            return 'Error', e.code
    #verify response csv isn't empty
    sniff = response.readline()
    if str(sniff) == '':
        return 'Not Available'
    #discard first line
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
        exchange = find_exchange(ticker)
        if exchange not in ['XNYS', 'XASE', 'XNAS', '']:
            return exchange
        #query morningstar for key ratios and check for errors
        self.keyratio_reader = query_morningstar(self, exchange, ticker,'&region=usa&culture=en-US&cur=USD&order=desc')
        if self.keyratio_flag[0] == '1':
            return self.keyratio_reader
        #Set flags and read data into memory upon successful query
        else:
            self.keyratio_flag[0] = '0'
            self.keyratio_flag[1] = ticker
            self.keyratio_data = [row for row in self.keyratio_reader]
    #check for existing datacode -> value map, if none exists then create it
    if not hasattr(self, 'datacode_map'):
        self.datacode_map = keyratio_datacode_map()
    #lookup and return value from map
    row, col = self.datacode_map[datacode]
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
def fetch_financials(symbol, datacode):
    """Get morningstar financial data and return desired element to user """
    if datacode < 1 or datacode > 126 :
        return 'Invalid Datacode'
    #query remote and catch errors
    exchange = find_exchange(symbol)
    if exchange == 'Ticker Not Supported':
        return exchange
    financial_dict = query_morningstar(exchange, symbol,'&region=usa&culture=en-US&cur=USD&reportType=is&period=12&dataType=A&order=desc&columnYear=5&rounding=3&view=raw&r=113199&denominatorView=raw&number=3')
    if financial_dict == 'Check Connection' or financial_dict == 'Not Available':
        return financial_dict     

    counter = 0
    skipped = 0
    #iterate through returned dict line by line
    for line in financial_dict:
        #skip lines with no data
        if counter == 3 or counter == 16 or counter == 19:
            skipped += 1
        else:
            for val in range(1, len(line)):
                #match year values to datacodes
                if datacode == val:
                    return financial_dict.fieldnames[val]
                #match data values to datacodes
                if (datacode - (counter - skipped) * (len(line)-1)) - (len(line)-1) == val:
                    data = line[financial_dict.fieldnames[val]]
                    return data
        counter += 1
    return 'No Data'