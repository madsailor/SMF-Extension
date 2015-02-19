import sys, csv, os, inspect
try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError
    from codecs import iterdecode
except:  
    from urllib2 import Request, urlopen, URLError
# Add current directory to path to import smf module
cmd_folder = os.path.realpath(os.path.abspath
                              (os.path.split(inspect.getfile
                                             ( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import smf   

def gen_test():
    test_data = []
    ticker_list = ["XOM"]
    for t in ticker_list:
        for d in range (1,164):
            test_data.append(t)
            test_data.append(d)
    return test_data

if __name__ == "__main__":
    smf = smf.SmfImpl(sys.argv)
    test_data = gen_test()
    for val in range (0,len(test_data),2):
        ticker = test_data[0 + val]
        datacode = test_data[1 + val]
        print (ticker, datacode,': ', smf.getMorningKey(ticker, datacode))