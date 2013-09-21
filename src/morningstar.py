import os
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
#todo : take fieldnames from discarded string rather than hardcode
        dict_fieldnames = [symbol,"TTM", "2012", "2011", "2010", "2009", "2008"]
        csvio = csv.DictReader(response)#, fieldnames=dict_fieldnames)
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
    elif exchange =='"NasdaqNM"':
        exchange = 'XNAS'
    elif exchange =='"NYSE"':
        exchange = 'XNYS'
    return exchange

def fetch_keyratios(symbol, datacode):
    exchange = find_exchange(symbol)
    #catch errors
    keyratio_dict = query_morningstar(exchange, symbol,'&region=usa&culture=en-US&cur=USD&order=desc')
    if keyratio_dict == 'Check Connection' or keyratio_dict == 'Not Available':
        return keyratio_dict    
    elif datacode < 1 or datacode > 1115 :
        return 'Invalid Datacode'
    counter = 0
    skipped = 0            
    for line in keyratio_dict:
    #match year values to datacodes
        for val in range(1, len(line)):
            if datacode == val:
                return keyratio_dict.fieldnames[val]
    #match data values to datacodes
        if counter == 15 or counter == 16 or counter == 27 or counter == 37 or counter == 38 or counter == 60 or counter == 68 or counter == 91 or counter == 97:
            skipped += 1
            counter += 1
        for val in range(1, len(line)):
            if (datacode - (counter * len(line) - skipped * len(line)) +(counter+ 1)) - len(line) == val:
                data = line[keyratio_dict.fieldnames[val]]
                return data
        counter += 1
    return 'No Data'

def query_local(a,b,c):
    cur_dir = os.getcwd()
    csv_file = open(cur_dir + '/keyratios.csv','r')
    csv_file.readline()
    csv_file.readline()
    csvio = csv.DictReader(csv_file)
    return csvio

def fetch_financials(symbol, datacode):
    exchange = find_exchange(symbol)
    #catch errors
    financial_dict = query_morningstar(exchange, symbol,'&region=usa&culture=en-US&cur=USD&reportType=is&period=12&dataType=A&order=desc&columnYear=5&rounding=3&view=raw&r=113199&denominatorView=raw&number=3')
    if financial_dict == 'Check Connection' or financial_dict == 'Not Available':
        return financial_dict    
    if datacode < 1 or datacode > 138 :
        return 'Invalid Datacode' 
    counter = 0
    for line in financial_dict:
        for val in range(1, len(line)):
            #match year values to datacodes
            if datacode == val:
                return financial_dict.fieldnames[val]
            #match data values to datacodes
#todo: doesn't read first line 'Revenue'
            if datacode - counter * (len(line)-1) == val:
                data = line[financial_dict.fieldnames[val]]
                return data
        counter += 1
    return 'No Data'