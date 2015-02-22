SMF Extension for LibreOffice Calc
===
The SMF extension allows you to create customized spreadsheets with stock market data directly from the web. Currently supported online sources include [Morningstar](http://morningstar.com) and [Yahoo Finance](http://finance.yahoo.com).

### Download   
You can download the current version of the SMF Extension here [![][shield:release-latest]][GIT:release]

The SMF extension can also be found on the [LibreOffice Extension Center](http://extensions.libreoffice.org/extension-center/smf-extension).

**NOTE**: The extension itself is SMF.oxt.  The example .ods worksheets demonstrate how to use the extension.

### Usage

The SMF Extension adds three new functions to Calc:

```GETYAHOO(Ticker,Datacode)```

```GETMORNINGKEY(Ticker,Datacode)```

```GETMORNINGFIN(Ticker,Datacode)```  


Quotes **must** be used when entering the ticker directly ex: ```GETYAHOO("AAPL",1)```, but are **not** needed when referencing another cell ex: ```GETYAHOO(A1,1)```.

In the latter case the data in A1 should be ```AAPL```, not ```"AAPL"```.

**NOTE**: The full set of datacodes are demonstrated in the example .ods worksheets included with the release.

###Support

For general support please visit the [forums](http://forum.openoffice.org/en/forum/index.php). If you find a bug or wish to request a feature please file an issue at the [issue tracker](http://github.com/madsailor/SMF-Extension/issues).

### Contribute

Help is always welcome with development.  If you would like to contribute you will need to fork the main repo, make your changes, and send a [pull request](http://github.com/madsailor/SMF-Extension/pulls) to have your changes moderated and merged back into the main repo. Details on that process can be found [here](https://help.github.com/articles/set-up-git/).  


### License

The SMF Extension is released under the [![][shield:LGPL3]][License:3.0] which in layman's terms means:  

* You are permitted to use, copy and redistribute the work "as-is".
* You may adapt, remix, transform and build upon the material, releasing any derivatives under your own name.
* You may use the material for commercial purposes as long as the derivative is licenced under the GPL.
* You must track changes you make in the source files.
* You must include or make available the source code with your release.

### Other Contributors and Thanks!
* Villeroy - conversion from string to float to make the extension useful
* karolus - optimization of keymapping code
* Corey Goldberg - Inspiration with the Yahoo portion of the extension

[GIT:release]: http://github.com/madsailor/SMF-Extension/releases/latest
[License:3.0]: http://www.gnu.org/licenses/lgpl.html
[shield:release-latest]: http://img.shields.io/github/release/madsailor/SMF-Extension.svg
[shield:LGPL3]: http://img.shields.io/badge/license-LGPL%20v.3-blue.svg"
