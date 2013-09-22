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
import csv
import urllib2
import ystockquote

def query_morningstar(exchange, symbol, url_ending): 
    if url_ending == '&region=usa&culture=en-US&cur=USD&order=desc':
        url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?&callback=?&t=%s:%s%s' % (exchange, symbol, url_ending)
        req = urllib2.Request(url)
        response = sniff_query(req)
        response.readline()
        csvio = csv.DictReader(response)
        return csvio
    else:
        url = 'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?&t=%s:%s%s' % (exchange, symbol, url_ending)
        req = urllib2.Request(url)
        response = sniff_query(req)
        csvio = csv.DictReader(response)
        return csvio
     
def sniff_query(req):
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError:
        return 'Check Connection'
    sniff = response.readline()
    if str(sniff) == '':
        return 'Not Available'
    return response

def find_exchange(symbol):
    exchange = ystockquote.get_stock_exchange(symbol)
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
        return 'Ticker Not Supported'

def fetch_keyratios(symbol, datacode):
    if datacode < 1 or datacode > 1115 :
        return 'Invalid Datacode'
    #query remote and catch errors
    exchange = find_exchange(symbol)
    if exchange == 'Ticker Not Supported':
        return exchange
    keyratio_dict = query_morningstar(exchange, symbol,'&region=usa&culture=en-US&cur=USD&order=desc')
    if keyratio_dict == 'Check Connection' or keyratio_dict == 'Not Available':
        return keyratio_dict
    #iterate through returned dict line by line    
    counter = 0
    skipped = 0            
    for line in keyratio_dict:
        if counter == 15 or counter == 16 or counter == 27 or counter == 37 or counter == 38 or counter == 60 or counter == 68 or counter == 91 or counter == 97:
            counter += 1
            skipped += 1
        else:
            for val in range(1, len(line)):
                #match year values to datacodes
                if datacode == val:
                    return keyratio_dict.fieldnames[val]
                #match data values to datacodes
                if (datacode - (counter * len(line) - skipped * len(line)) +(counter+ 1)) - len(line) == val:
                    data = line[keyratio_dict.fieldnames[val]]
                    return data
        counter += 1
    return 'No Data'

def fetch_financials(symbol, datacode):
    if datacode < 1 or datacode > 120 :
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
#todo: doesn't read first line 'Revenue'
                if datacode - (counter - skipped) * (len(line)-1) == val:
                    data = line[financial_dict.fieldnames[val]]
                    return data
        counter += 1
    return 'No Data'
