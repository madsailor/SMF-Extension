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

# Add current directory to path to import ystockquote module
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import ystockquote
import morningstar

class SmfImpl( unohelper.Base, XSmf ):
    def __init__( self, ctx ):
        self.ctx = ctx

    def getYahoo( self, ticker, datacode ):
        if datacode < 1 or datacode > 83 :
            return 'Invalid Datacode'
        elif datacode == 1 :
            return ystockquote.get_dividend_yield(ticker)
        elif datacode == 2 :
            return ystockquote.get_dividend_per_share(ticker)
        elif datacode == 3 :
            return ystockquote.get_ask_realtime(ticker)
        elif datacode == 4 :
            return ystockquote.get_dividend_pay_date(ticker)
        elif datacode == 5 :
            return ystockquote.get_bid_realtime(ticker)
        elif datacode == 6 :
            return ystockquote.get_ex_dividend_date(ticker)
        elif datacode == 7 :
            return ystockquote.get_previous_close(ticker)
        elif datacode == 8 :
            return ystockquote.get_today_open(ticker)
        elif datacode == 9 :
            return ystockquote.get_change(ticker)
        elif datacode == 10 :
            return ystockquote.get_last_trade_date(ticker)
        elif datacode == 11 :
            return ystockquote.get_change_percent_change(ticker)
        elif datacode == 12 :
            return ystockquote.get_trade_date(ticker)
        elif datacode == 13 :
            return ystockquote.get_change_realtime(ticker)
        elif datacode == 14 :
            return ystockquote.get_last_trade_time(ticker)
        elif datacode == 15 :
            return ystockquote.get_change_percent_realtime(ticker)
        elif datacode == 16 :
            return ystockquote.get_change_percent(ticker)
        elif datacode == 17 :
            return ystockquote.get_after_hours_change(ticker)
        elif datacode == 18 :
            return ystockquote.get_change_200_sma(ticker)
        elif datacode == 19 :
            return ystockquote.get_commission(ticker)
        elif datacode == 20 :
            return ystockquote.get_percent_change_200_sma(ticker)
        elif datacode == 21 :
            return ystockquote.get_todays_low(ticker)
        elif datacode == 22 :
            return ystockquote.get_change_50_sma(ticker)
        elif datacode == 23 :
            return ystockquote.get_todays_high(ticker)
        elif datacode == 24 :
            return ystockquote.get_percent_change_50_sma(ticker)
        elif datacode == 25 :
            return ystockquote.get_last_trade_realtime_time(ticker)
        elif datacode == 26 :
            return ystockquote.get_50_sma(ticker)
        elif datacode == 27 :
            return ystockquote.get_last_trade_time_plus(ticker)
        elif datacode == 28 :
            return ystockquote.get_200_sma(ticker)
        elif datacode == 29 :
            return ystockquote.get_last_trade_price(ticker)
        elif datacode == 30 :
            return ystockquote.get_1_year_target(ticker)
        elif datacode == 31 :
            return ystockquote.get_todays_value_change(ticker)
        elif datacode == 32 :
            return ystockquote.get_holdings_gain_percent(ticker)
        elif datacode == 33 :
            return ystockquote.get_todays_value_change_realtime(ticker)
        elif datacode == 34 :
            return ystockquote.get_annualized_gain(ticker)
        elif datacode == 35 :
            return ystockquote.get_price_paid(ticker)
        elif datacode == 36 :
            return ystockquote.get_holdings_gain(ticker)
        elif datacode == 37 :
            return ystockquote.get_todays_range(ticker)
        elif datacode == 38 :
            return ystockquote.get_holdings_gain_percent_realtime(ticker)
        elif datacode == 39 :
            return ystockquote.get_todays_range_realtime(ticker)
        elif datacode == 40 :
            return ystockquote.get_holdings_gain_realtime(ticker)
        elif datacode == 41 :
            return ystockquote.get_52_week_high(ticker)
        elif datacode == 42 :
            return ystockquote.get_more_info(ticker)
        elif datacode == 43 :
            return ystockquote.get_52_week_low(ticker)
        elif datacode == 44 :
            return ystockquote.get_market_cap(ticker)
        elif datacode == 45 :
            return ystockquote.get_change_from_52_week_low(ticker)
        elif datacode == 46 :
            return ystockquote.get_market_cap_realtime(ticker)
        elif datacode == 47 :
            return ystockquote.get_change_from_52_week_high(ticker)
        elif datacode == 48 :
            return ystockquote.get_float_shares(ticker)
        elif datacode == 49 :
            return ystockquote.get_percent_change_from_52_week_low(ticker)
        elif datacode == 50 :
            return ystockquote.get_company_name(ticker)
        elif datacode == 51 :
            return ystockquote.get_percent_change_from_52_week_high(ticker)
        elif datacode == 52 :
            return ystockquote.get_notes(ticker)
        elif datacode == 53 :
            return ystockquote.get_52_week_range(ticker)
        elif datacode == 54 :
            return ystockquote.get_shares_owned(ticker)
        elif datacode == 55 :
            return ystockquote.get_stock_exchange(ticker)
        elif datacode == 56 :
            return ystockquote.get_shares_outstanding(ticker)
        elif datacode == 57 :
            return ystockquote.get_volume(ticker)
        elif datacode == 58 :
            return ystockquote.get_ask_size(ticker)
        elif datacode == 59 :
            return ystockquote.get_bid_size(ticker)
        elif datacode == 60 :
            return ystockquote.get_last_trade_size(ticker)
        elif datacode == 61 :
            return ystockquote.get_ticker_trend(ticker)
        elif datacode == 62 :
            return ystockquote.get_average_daily_volume(ticker)
        elif datacode == 63 :
            return ystockquote.get_trade_links(ticker)
        elif datacode == 64 :
            return ystockquote.get_order_book_realtime(ticker)
        elif datacode == 65 :
            return ystockquote.get_high_limit(ticker)
        elif datacode == 66 :
            return ystockquote.get_eps(ticker)
        elif datacode == 67 :
            return ystockquote.get_low_limit(ticker)
        elif datacode == 68 :
            return ystockquote.get_eps_estimate_current_year(ticker)
        elif datacode == 69 :
            return ystockquote.get_holdings_value(ticker)
        elif datacode == 70 :
            return ystockquote.get_eps_estimate_next_year(ticker)
        elif datacode == 71 :
            return ystockquote.get_holdings_value_realtime(ticker)
        elif datacode == 72 :
            return ystockquote.get_eps_estimate_next_quarter(ticker)
        elif datacode == 73 :
            return ystockquote.get_revenue(ticker)
        elif datacode == 74 :
            return ystockquote.get_book_value(ticker)
        elif datacode == 75 :
            return ystockquote.get_ebitda(ticker)
        elif datacode == 76 :
            return ystockquote.get_price_sales(ticker)
        elif datacode == 77 :
            return ystockquote.get_price_book(ticker)
        elif datacode == 78 :
            return ystockquote.get_pe(ticker)
        elif datacode == 79 :
            return ystockquote.get_pe_realtime(ticker)
        elif datacode == 80 :
            return ystockquote.get_peg(ticker)
        elif datacode == 81 :
            return ystockquote.get_price_eps_estimate_current_year(ticker)
        elif datacode == 82 :
            return ystockquote.get_price_eps_estimate_next_year(ticker)
        elif datacode == 83 :
            return ystockquote.get_short_ratio(ticker)

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
