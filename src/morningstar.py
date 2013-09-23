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
    if datacode < 1 or datacode > 990:
        return 'Invalid Datacode'
    #query remote and catch errors
    exchange = find_exchange(symbol)
    if exchange == 'Ticker Not Supported':
        return exchange
    keyratio_dict = query_morningstar(exchange, symbol,'&region=usa&culture=en-US&cur=USD&order=desc')
    if keyratio_dict == 'Check Connection' or keyratio_dict == 'Not Available':
        return keyratio_dict    
    counter = 0
    skipped = 0
    skip_lines = [15, 16, 26, 36, 37, 57, 58, 64, 65, 86, 91, 92]            
    #iterate through returned dict line by line
    for line in keyratio_dict:
        for item in skip_lines:
            if counter == item:
                skipped += 1
        for val in range(1, len(line)):
            #match year values to datacodes
            if datacode == val:
                return keyratio_dict.fieldnames[val]
            #match data values to datacodes
            if (datacode - (counter - skipped) * (len(line)-1)) - (len(line)-1) == val:
                data = line[keyratio_dict.fieldnames[val]]
                return data
        counter += 1
    return 'No Data'

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