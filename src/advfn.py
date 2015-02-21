import yahoo
import parser
from urllib.request import Request, urlopen
from urllib.error import URLError

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
            data = parse_advfn(self, self.advfn_reader.decode('utf-8'))
    return data

def parse_advfn(self, u_data):
    p = parser.HTMLTableParser()
    p.feed(u_data)
    p_data = p.tables
    return p_data

def query_advfn(self, ticker):
    """Query ADVFN for the data we want"""
    exchange = advfn_exchange(self, ticker)
    if exchange not in ['NYSE', 'NASDAQ', 'AMEX']:
        return exchange
    url = 'http://www.advfn.com/exchanges/%s/%s/financials?btn=annual_reports&mode=company_data' % (exchange, ticker)
    req = Request(url)
    try:
        response = urlopen(req)
        resp_data = response.read()
    except URLError as e:
        self.advfn_flag[0] = '1'
        if hasattr(e, 'reason'):
            return e.reason
        elif hasattr(e,'code'):
            return 'Error', e.code
    return resp_data   

def advfn_exchange(self, ticker):
    """Determine exchange ticker is traded on so we can query advfn"""
    exchange = yahoo.fetch_data(self, ticker, 54)    
    if exchange =='NasdaqNM':
        exchange = 'NASDAQ'
    return exchange