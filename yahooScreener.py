import os, datetime, re
from time import sleep
from finviz.screener import Screener
from urllib import request as r
from bs4 import BeautifulSoup

# Filter for Stocks
filters = ['sh_price_u5','ta_gap_d5','ta_rsi_os30','ft=3']
stocks = Screener(filters=filters, order="price")
tickers = [ticker['Ticker'] for ticker in stocks]

def group(lst, n):
  for i in range(0, len(lst), n):
    val = lst[i:i+n]
    if len(val) == n:
      yield tuple(val)

def getData(tickers, ctime):
    for ticker in tickers:
        html = r.urlopen(f"https://finance.yahoo.com/quote/{ ticker }")
        soup = BeautifulSoup(html, 'html.parser')

        quoteHeader = soup.findAll('div', attrs={"id":"quote-header-info"})
        current_price = quoteHeader[0].findAll(attrs={"data-reactid":"14"})[0].get_text()
        tds = list(group(soup.findAll(lambda tag: tag.name == 'td' and 'data-reactid' in tag.attrs), 2))
        texts = { t[0].get_text(): t[1].get_text() for t in tds if 'Open' in t[0].get_text() or 'Volume' in t[0].get_text() or 'Avg. Volume' in t[0].get_text() or 'Bid' in t[0].get_text() or 'Ask' in t[0].get_text()}

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

        gappers = open('gappers.csv', 'a+')
        gappers_read = open('gappers.csv','r')
        lines = len(gappers_read.readlines())
        gappers_read.close()
        if lines > 0:
            gappers.write(f"{','.join(data.values())}\n")
        else:
            gappers.write(f"{','.join(data.keys())}\n")
            gappers.write(f"{','.join(data.values())}\n")
        print(f'recorded data for time { ctime }')

def recordData():
    check = True
    # adjusted to MST, no daylight savings time included.
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