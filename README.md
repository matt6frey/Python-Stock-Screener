# Python Stock Screener

This is a stock screener that harnesses the Finviz Module ([FinViz - Repo](https://github.com/mariostoev/finviz), [Finviz - PiPy](https://pypi.org/project/finviz/)), it then uses Beautiful Soup collect data and export it into a CSV file.

## Installation & Usage

**Install**

`pip install -r requirements.txt`


**Usage**

`python yahooScreener.py` in your terminal. The script will save the results within the same directory, inside a CSV called 'gappers.csv'. 

Alternatively, you can use the `--filename=<filename>` to change the filename, `--dir=<dir>` to change the directory path and `--ext=<ext>` to change the extension of the file.

i.e. `python yahooScreener.py --filename=stocks --dir=~/Desktop/Stocks/ --ext=txt`

## Screener Options

*Coming Soon*

## Modules

- FinViz
- BeautifulSoup
- URLLIB

## Future Goals

1. Assign existing script to backend API
2. Create Ionic App that will use API and provide quick menu for screening, and Stock data push notifications and records.
