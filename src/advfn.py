import csv, sys, urllib2
from bs4 import BeautifulSoup

class SmfImpl():
    """Define the main class for the SMF extension """
    def __init__( self, ctx ):
        self.ctx = ctx
        self.advfn_flag = ['0', '']
        self.yahoo_flag = ['0', '']

    def getADVFN( self, ticker, datacode ):
        return fetch_advfn(self, ticker, datacode)

def fetch_advfn(self, ticker, datacode):
    """Get ADVFN data and return desired element to user """
    if datacode < 1 or datacode > 2810 :
        return 'Invalid Datacode'
    if self.advfn_flag[0] == '1' or self.advfn_flag[1] != ticker:
        self.advfn_reader = query_advfn(self, ticker)
        if self.advfn_flag[0] == '1':
            return self.advfn_reader
        #Set flags and parse data upon successful query
        else:
            self.advfn_data = []
            self.advfn_flag[0] = '0'
            self.advfn_flag[1] = ticker
            advfn_soup = BeautifulSoup(self.advfn_reader)
            #find the table with the data we want
            parent_tag = advfn_soup.find_all('table',{'align':'center'})
            #find the data elements we want
            for p_tag in parent_tag:
#                header_tag = tag.find_all("td", {"align":"left"}) #shows data type (row header)       
                data_tag = p_tag.find_all("td", {"align":"right"}) #shows data
                for d_tag in data_tag:
                    self.advfn_data.append(d_tag.text)
    return self.advfn_data[datacode]

def query_advfn(self, ticker):
    """Query ADVFN for the data we want"""
    exchange = advfn_exchange(self, ticker)
    if exchange not in ['NYSE', 'NASDAQ', 'AMEX']:
        return exchange
    url = 'http://www.advfn.com/exchanges/%s/%s/financials?btn=start_date&start_date=10&mode=annual_reports' % (exchange, ticker)
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError as e:
        self.advfn_flag[0] = '1'
        if hasattr(e, 'reason'):
            return e.reason
        elif hasattr(e,'code'):
            return 'Error', e.code
    return response   

def advfn_exchange(self, ticker):
    """Determine exchange ticker is traded on so we can query advfn"""
    exchange = fetch_data(self, ticker, 54)    
    if exchange =='NasdaqNM':
        exchange = 'NASDAQ'
    return exchange
    
def fetch_data(self, ticker, datacode):
    if datacode < 1 or datacode > 81 :
        return 'Invalid Datacode'
    query_list = ['y','d','b2','r1','b3','q','p','o','c1','d1','c','d2','c6','t1','k2','p2','c8','m5','c3','m6','g','m7','h','m8','k1','m3','l','m4','l1','t8','w1','g1','w4','g3','p1','g4','m','g5','m2','g6','k','v','j','j1','j5','j3','k4','j6','n','k5','n4','w','s1','x','v','a5','b6','k3','t7','a2','t6','i5','l2','e','l3','e7','v1','e8','v7','e9','s6','b4','j4','p5','p6','r','r2','r5','r6','r7','s7']
    stat = ''.join(query_list)
    if self.yahoo_flag[0] == '1' or self.yahoo_flag[1] != ticker:
        self.yahoo_reader = query_yahoo(self, ticker, stat)
        if self.yahoo_flag[0] == '1':
            return self.yahoo_reader
        #Set flags upon successful query
        else:
            self.yahoo_flag[0] = '0'
            self.yahoo_flag[1] = ticker
            for row in self.yahoo_reader:
                self.yahoo_data = row
    return self.yahoo_data[datacode-1]

def query_yahoo(self, ticker, stat): 
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (ticker, stat)
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError as e:
        self.yahoo_flag[0] = '1'
        if hasattr(e, 'reason'):
            return e.reason
        elif hasattr(e,'code'):
            return 'Error', e.code
    return csv.reader(response) 

if __name__ == "__main__":
    smf = SmfImpl(sys.argv)
    ticker = "XOM"
    for datacode in xrange (1,2812):
        print ticker, datacode,': ', smf.getADVFN(ticker, datacode)