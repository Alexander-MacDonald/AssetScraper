import CFG
import time
import random
import requests 

def getStockPrice(ticker):
    url = CFG.LIVEPRICEQUERYURL.format(ticker=ticker)
    response = requests.get(url, headers=CFG.HEADERS)
    data = response.json()
    return data["chart"]["result"][0]["meta"]["regularMarketPrice"]

def getStockPrices(tickers):
    prices = []
    for ticker in tickers:
        time.sleep(random.uniform(0.1, 1.5))
        prices.append((ticker, getStockPrice(ticker)))
    return prices