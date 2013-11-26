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

def query_morningstar(self, exchange, symbol, url_ending): 
    if url_ending == '&region=usa&culture=en-US&cur=USD&order=desc':
        url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?&callback=?&t=%s:%s%s' % (exchange, symbol, url_ending)
    else:
        url = 'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?&t=%s:%s%s' % (exchange, symbol, url_ending)
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError as e:
        self.flag[0] = '1'
        if hasattr(e, 'reason'):
            return e.reason
        elif hasattr(e,'code'):
            return 'Error', e.code
    sniff = response.readline()
    if str(sniff) == '':
        return 'Not Available'
    response.readline()
    return csv.reader(response)

def find_exchange(ticker):
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

def fetch_keyratios(self, ticker, datacode):
    if datacode < 1 or datacode > 990:
        return 'Invalid Datacode'
    #check whether flags indicate that we already have the data we need
    if self.flag[0] == '1' or self.flag[1] != ticker:
        #query yahoo for exchange and check for errors
        exchange = find_exchange(ticker)
        if exchange not in ['XNYS', 'XASE', 'XNAS', '']:
            return exchange
        #query morningstar for key financials and check for errors
        self.csv_reader = query_morningstar(self, exchange, ticker,'&region=usa&culture=en-US&cur=USD&order=desc')
        if self.flag[0] == '1':
            return self.csv_reader
        #Set flags and read data into memory upon successful query
        else:
            self.flag[0] = '0'
            self.flag[1] = ticker
            self.data = [row for row in self.csv_reader]
    return sort_keyratios(self, datacode)

def sort_keyratios(self, datacode):
    #define rows that have no useful data   
    skip_list = [16,17,18,28,29,38,39,40,41,46,51,56,61,62,63,69,70,71,92,93,98,99,100]
    skipped = 0
    # match datacode to row, column and return data in that position of list
    for row in range(0,109):
        if row in skip_list:
            skipped+=11
            continue
        for col in range(0,12):
            if datacode == col+(11*row)-skipped:
                return self.data[row][col]

#TODO: Update getMorningFin to recycle local data like getMorningKey
def fetch_financials(symbol, datacode):
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