import uno
import unohelper
from com.smf.ticker.getinfo import XYahoo
# Add current directory to path to import ystockquote module
import os, sys, inspect
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)
import ystockquote

class YahooImpl( unohelper.Base, XYahoo ):
	def __init__( self, ctx ):
		self.ctx = ctx

	def getYahoo( self, ticker, datacode ):
		if datacode < 1 or datacode > 20 :
			return None
		elif datacode == 1 :
			return ystockquote.get_price(ticker)
		elif datacode == 2 :
			return ystockquote.get_change(ticker)
		elif datacode == 3 :
			return ystockquote.get_volume(ticker)
		elif datacode == 4 :
			return ystockquote.get_avg_daily_volume(ticker)
		elif datacode == 5 :
			return ystockquote.get_stock_exchange(ticker)
		elif datacode == 6 :
			return ystockquote.get_market_cap(ticker)
		elif datacode == 7 :
			return ystockquote.get_book_value(ticker)
		elif datacode == 8 :
			return ystockquote.get_ebitda(ticker)
		elif datacode == 9 :
			return ystockquote.get_dividend_per_share(ticker)
		elif datacode == 10 :
			return ystockquote.get_dividend_yield(ticker)
		elif datacode == 11 :
			return ystockquote.get_earnings_per_share(ticker)
		elif datacode == 12 :
			return ystockquote.get_52_week_high(ticker)
		elif datacode == 13 :
			return ystockquote.get_52_week_low(ticker)
		elif datacode == 14 :
			return ystockquote.get_50day_moving_avg(ticker)
		elif datacode == 15 :
			return ystockquote.get_200day_moving_avg(ticker)
		elif datacode == 16 :
			return ystockquote.get_price_earnings_ratio(ticker)
		elif datacode == 17 :
			return ystockquote.get_price_earnings_growth_ratio(ticker)
		elif datacode == 18 :
			return ystockquote.get_price_sales_ratio(ticker)
		elif datacode == 19 :
			return ystockquote.get_price_book_ratio(ticker)
		elif datacode == 20 :
			return ystockquote.get_short_ratio(ticker)

def createInstance( ctx ):
	return YahooImpl( ctx )

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation( \
	createInstance,"com.smf.ticker.getinfo.python.YahooImpl",
		("com.sun.star.sheet.AddIn",),)
