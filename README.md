Stock Market Data for LibreOffice Calc
================================

*A compiled and ready-to-install version of this extension is available at the [LibreOffice Extension Center](http://extensions.libreoffice.org/extension-center/smf-extension/).*

Currently the SMF Extension supports retrieving data from Morningstar and Yahoo Finance. I hope that providing the code openly will allow others, who may have the time or skill, to implement additional functionality.

Usage
------------------------
The SMF Extension adds three new functions to Calc.  These functions can be used as follows:  

    =GETYAHOO(Ticker,Datacode)
    =GETMORNINGKEY(Ticker,Datacode)
    =GETMORNINGFIN(Ticker,Datacode)  

Where *Ticker* is the standard symbol ex. AAPL and *Datacode* is the data element desired.  

Quotes *__MUST__* be used when entering the ticker symbol directly into the function:
  
    =GETYAHOO("AAPL",1)  
But are *not* needed when referencing another cell:
  
    =GETYAHOO(A1,1)  
In the latter case the data in A1 should be AAPL *not* "AAPL"  

The Datacode lists:
-----------------------
*The full code lists are demonstrated in individual spreadsheets found in the /examples directory*  

*__NOTE:__ These files call the new functions many times and may be slow to load depending on your internet connection and computer hardware. Please be patient.*  

Additional sources to implement 
-------------------------
* For historical company financial data: The SEC's [EDGAR Database](http://www.sec.gov/edgar/searchedgar/companysearch.html)  
Use of the XBRL markup looks like a promising avenue for more recent (~5yr) filings.  Outside that may require some serious regex muscle.

* For current and historical market data: The [NASDAQ Database](http://www.nasdaq.com/symbol/ge/historical)  

* There are many other sites such as [ADVFN](http://www.advfn.com/), [Finviz](http://finviz.com/), and [Marketwatch](http://www.marketwatch.com/) that provide useful data.  

About
-------------------------
The SMF extension is written in [Python](www.python.org).  Thanks to Corey Goldberg's [ystockquote](https://github.com/cgoldberg/ystockquote) for inspiration with the Yahoo portion of the SMF Extension.
