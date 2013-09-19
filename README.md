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

*The full code list is demonstrated in the YahooExample.ods spreadsheet*  

Code|Element||Code|Element||Code|Element
----|----|----|----|----|----|----|----
1|Price||29|Last Trade (Price Only)||57|Volume
2||Dividend per Share||30|1 yr Target Price||58|Ask Size
3|Ask (Realtime)||31|Todays Value Change||59|Bid Size
4|Dividend Pay Date||32|Holdings Gain Percent||60|Last Trade Size
5|Bid (Realtime)||33|Todays Value Change (Realtime)||61|Ticker Trend
6|Ex-Dividend Date||34|Annualized Gain||62|Average Daily Volume
7|Previous Close||35|Price Paid||63|Trade Links
8|Open||36|Holdings Gain||64|Order Book (Realtime)
9|Change||37|Todays Range||65|High Limit
10|Last Trade Date||38|Holdings Gain Percent (Realtime)||66|EPS
11|Change & Percent Change||39|Todays Range (Realtime)||67|Low Limit
12|Trade Date||40|Holdings Gain (Realtime)||68|EPS Estimate Current Year
13|Change (Realtime)||41|52 Week High||69|Holdings Value
14|Last Trade Time||42|More Info||70|EPS Estimate Next Year
15|Change Percent (Realtime)||43|52 week Low||71|Holdings Value (Realtime)
16|Change in Percent||44|Market Cap||72|EPS Estimate Next Quarter
17|After Hours Change (Realtime)||45|Change From 52 Week Low||73|Revenue
18|Change From 200 Day Moving Average||46|Market Cap (Realtime)||74|Book Value
19|Commission||47|Change From 52 week High||75|EBITDA
20|Percent Change From 200 Day Moving Average||48|Float Shares||76|Price / Sales
21|Todays Low||49|Percent Change From 52 week Low||77|Price / Book
22|Change From 50 Day Moving Average||50|Company Name||78|P/E Ratio
23|Todays High||51|Percent Change From 52 week High||79|P/E Ratio (Realtime)
24|Percent Change From 50 Day Moving Average||52|Notes||80|PEG Ratio
25|Last Trade (Realtime) With Time||53|52 week Range||81|Price / EPS Estimate Current Year
26|50 Day Moving Average||54|Shares Owned||82|Price / EPS Estimate Next Year
27|Last Trade (With Time)||55|Stock Exchange||83|Short Ratio
28|200 Day Moving Average||56|Shares Outstanding|||


Additional sources to (hopefully) be implemented 
-------------------------
* For historical company financial data: The SEC's [EDGAR Database](http://www.sec.gov/edgar/searchedgar/companysearch.html)  
Use of the XBRL markup looks like a promising avenue for more recent (~5yr) filings.  Outside that may require some serious regex muscle.

* For current and historical market data: The [NASDAQ Database](http://www.nasdaq.com/symbol/ge/historical)  

* There are many other quality sites such as [ADVFN](http://www.advfn.com/), [Finviz](http://finviz.com/), and [Marketwatch](http://www.marketwatch.com/) that provide useful data.

* For those with Excel coding experience there is a tremendous amount of functionality that may be ported from Randy Harmelink's [Excel SMF AddIn](http://groups.yahoo.com/neo/groups/smf_addin/info)


About
-------------------------
The SMF Extension is powered by Corey Goldberg's [ystockquote](https://github.com/cgoldberg/ystockquote) and written in [Python](www.python.org).

