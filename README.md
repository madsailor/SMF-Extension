Stock Market Data for LibreOffice Calc
================================

*A compiled and ready-to-install version of this extension is available at the [LibreOffice Extension Center](http://extensions.libreoffice.org/extension-center).*

Currently the SMF Extension supports retrieving data only from Yahoo Finance. I hope that providing the code openly will allow others who may have more time or skill to implement additional functionality.

Usage
------------------------
The SMF Extension adds a new function to Calc titled GETYAHOO.  This function can be used as follows:  

    =GETYAHOO(ticker,datacode)  

Where *ticker* is the standard symbol ex. AAPL and *datacode* is the data element desired.

The current datacode list:
-------------

Code|Element||Code|Element
----|----|----|----|----
1|Price||11|EPS
2|Change||12|52 Week High
3|Volume||13|52 Week Low
4|Avg.Volume||14|50 Day SMA
5|Exchange||15|200 Day SMA
6|Market Cap||16|PE Ratio
7|Book Value||17|PEG Ratio
8|EBITDA||18|PriceSales
9|Dividends Per Share||19|PriceBook
10|Dividend Yield||20|Short Ratio

Additional sources to (hopefully) be implemented 
-------------------------
* For historical company financial data: The SEC's [EDGAR Database](http://www.sec.gov/edgar/searchedgar/companysearch.html)  
Use of the XBRL markup looks like a promising avenue for more recent (~5yr) filings.  Outside that may require some serious regex muscle.

* For current and historical market data: The [NASDAQ Database](http://www.nasdaq.com/symbol/ge/historical)  

* There are many other quality sites such as [ADVFN](http://www.advfn.com/), [Finviz](http://finviz.com/), and [Marketwatch](http://www.marketwatch.com/) that provide useful data.

* For those with Excel coding experience there is a tremenous amount of functionality that may be ported from Randy Harmelink's [Excel SMF AddIn](http://groups.yahoo.com/neo/groups/smf_addin/info)


About
-------------------------
The SMF Extension is powered by Corey Goldberg's [ystockquote](https://github.com/cgoldberg/ystockquote) and written in [Python](www.python.org).

