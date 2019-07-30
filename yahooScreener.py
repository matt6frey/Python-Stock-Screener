import os, datetime, re, sys
from time import sleep
from finviz.screener import Screener
from urllib import request as r
from bs4 import BeautifulSoup

def check_args(args, flag):
    '''Cycles through sys args and returns None or value of Arg'''
    value = None
    if len(args):
        for arg in args:
            if flag in arg:
                value = get_arg(arg)
    return value

def get_arg(arg):
    return arg.split('=')[1] if arg else ''

filename = check_defaults(check_args(sys.argv, 'filename'),'filename')
path = check_defaults(check_args(sys.argv, 'dir'),'dir')
ext = check_defaults(check_args(sys.argv, 'ext'),'ext')
target_path = f'{path}{filename}.{ext}'

def check_defaults(value, flag):
    defaults = {
        'filename': 'gappers',
        'dir': os.getcwd(),
        'ext':'csv'
    }
    return value if value != None else defaults[flag]

# Filter for Stocks
filters = ['sh_price_u5','ta_gap_d5','ta_rsi_os30','ft=3']
stocks = Screener(filters=filters, order="price")
tickers = [ticker['Ticker'] for ticker in stocks]

def group(lst, n):
  '''Creates an Array of 2 values: key & value from BS4 extracted data.'''
  for i in range(0, len(lst), n):
    val = lst[i:i+n]
    if len(val) == n:
      yield tuple(val)

def scan_columns(value):
    '''Verify Column is present from Current TD element.'''
    columns = ['Open','Close','Volume','Avg. Volume','Bid','Ask']

    for col in columns:
        return True if col in value

def getData(tickers, ctime):
    for ticker in tickers:
        html = r.urlopen(f"https://finance.yahoo.com/quote/{ ticker }")
        soup = BeautifulSoup(html, 'html.parser')

        quoteHeader = soup.findAll('div', attrs={"id":"quote-header-info"})
        current_price = quoteHeader[0].findAll(attrs={"data-reactid":"14"})[0].get_text() # specific TD from Yahoo Finance.
        tds = list(group(soup.findAll(lambda tag: tag.name == 'td' and 'data-reactid' in tag.attrs), 2))
        texts = { t[0].get_text(): t[1].get_text() for t in tds if scan_columns(t[0].get_text()) }

        data = {
            "current time": ctime.strftime("%Y %m %d - %H:%M:%S"),
            "ticker": ticker,
            "current price": current_price,
            "open": texts['Open'],
            "bid": texts['Bid'],
            "ask": texts['Ask'],
            "volume": texts['Volume'],
            "average volume": f"'{texts['Avg. Volume']}'",
            "close": current_price if ctime.hour == 17 or 19 else None
        }

        if os.path.exists(path):
            gappers = open(target_path, 'a+')
            gappers_read = open(target_path,'r')
            lines = len(gappers_read.readlines())
            gappers_read.close()
            if lines > 0:
                gappers.write(f"{','.join(data.values())}\n")
            else:
                gappers.write(f"{','.join(data.keys())}\n")
                gappers.write(f"{','.join(data.values())}\n")
            print(f'recorded data for time { ctime }')
        else:
            raise OSError(f"Path: {target_path} doesn't exist...")

def recordData():
    check = True
    # adjusted from EST to MST, no daylight savings time included.
    while check:
        current_time = datetime.datetime.now()
        if current_time.hour >= 7 and current_time.hour <= 13:
            if (current_time.hour == 7 and current_time.minute >= 30 and current_time.minute <= 59) or (current_time.hour >= 8 and current_time.hour <= 15):
                getData(tickers, current_time)
            sleep(60*15) # check every 15 minutes
        else:
            check = False

    print('Finished recording for today...')

recordData()