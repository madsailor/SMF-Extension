#  smftest.py - Test SMF functions through the Python console
#
#  Copyright (c) 2015 David Capron (drbluesman@yahoo.com)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
from __future__ import print_function
import sys
import os
import inspect
import getopt
#Add path to LO/OO components.
if sys.version_info.major == 3:
    sys.path.append('/usr/lib/libreoffice/program')
else:
    sys.path.append('/usr/lib/openoffice4/program')
    if getattr(os.environ, 'URE_BOOTSTRAP', None) is None:
        os.environ['URE_BOOTSTRAP'] = "vnd.sun.star.pathname:/usr/lib/"\
                                      "openoffice4/program/fundamentalrc"
# Add current directory to path to import smf module
cmd_folder = os.path.realpath(os.path.abspath
                              (os.path.split(inspect.getfile
                                             ( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)  
import smf

def main(argv):
    main_smf = smf.SmfImpl(argv)
    arg_funct = ''
    arg_ticker = ''
    try:
        opts, args = getopt.getopt(argv, "f:t:",["function=","ticker="])
    except getopt.GetoptError:
        usage(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-f", "--function"):
            arg_funct = arg
        elif opt in ("-t", "--ticker"):
            arg_ticker = arg
    print ("Function tested is", arg_funct)
    print ("Ticker used is", arg_ticker)
    if arg_funct == "morningkey":
        key_test(main_smf, arg_ticker)
    elif arg_funct == "morningfin":
        fin_test(main_smf, arg_ticker, '')
    elif arg_funct == "morningqfin":
        fin_test(main_smf, arg_ticker, 'qtr')
    elif arg_funct == "yahoo":
        yahoo_test(main_smf, arg_ticker)
    elif arg_funct == "advfn":
        advfn_test(main_smf, arg_ticker)
    sys.exit(2)

def key_test(smf_py, ticker):
    test_data = []
    for d in range (1,948):
        test_data.append(ticker)
        test_data.append(d)
    for val in range (0,len(test_data),2):
        datacode = test_data[1 + val]
        print (datacode,': ', smf_py.getMorningKey(ticker, datacode))
    sys.exit()

def fin_test(smf_py, ticker, fin_type):
    test_data = []
    func_call = smf_py.getMorningFin
    if fin_type == 'qtr':
        func_call = smf_py.getMorningQFin
    for d in range (1,164):
        test_data.append(ticker)
        test_data.append(d)
    for val in range (0,len(test_data),2):
        datacode = test_data[1 + val]
        print (datacode,': ', func_call(ticker, datacode))
    sys.exit()

def yahoo_test(smf_py, ticker):
    test_data = []
    for d in range (1,55):
        test_data.append(ticker)
        test_data.append(d)
    for val in range (0,len(test_data),2):
        datacode = test_data[1 + val]
        print (datacode,': ', smf_py.getYahoo(ticker, datacode))
    sys.exit()
    
def advfn_test(smf_py, ticker):
    test_data = []
    for d in range (1,5293):
#    for d in range (1,26):
        test_data.append(ticker)
        test_data.append(d)
    for val in range (0,len(test_data),2):
        datacode = test_data[1 + val]
        print (datacode,': ', smf_py.getADVFN(ticker, datacode))
    sys.exit()
        
def usage(err):
    print ("Usage: smftest.py -f <function> -t <ticker>")
    print ('Available functions are morningkey, morningfin, morningqfin, yahoo'
           'and advfn')
    if err == 2:
        sys.exit(2)
    else:
        sys.exit()
        
if __name__ == "__main__":
    main(sys.argv[1:])