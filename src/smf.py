#  smf.py - class to implement new functions for SMF Extension
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
import uno
import unohelper
from com.smf.ticker.getinfo import XSmf
import os, sys, inspect

# Add current directory to path to import yahoo and morningstar modules
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import yahoo
import morningstar

class SmfImpl( unohelper.Base, XSmf ):
    def __init__( self, ctx ):
        self.ctx = ctx

    def getYahoo( self, ticker, datacode ):
        data_element = yahoo.fetch_data(ticker, datacode)
        return data_element

    def getMorningKey( self, ticker, datacode ):
        return morningstar.fetch_keyratios(ticker, datacode)
    def getMorningFin( self, ticker, datacode ):
        return morningstar.fetch_financials(ticker, datacode)

def createInstance( ctx ):
    return SmfImpl( ctx )

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation( \
    createInstance,"com.smf.ticker.getinfo.python.SmfImpl",
        ("com.sun.star.sheet.AddIn",),)