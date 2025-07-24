import json

def getTickers():
    tickers = set()

    #get tickers from holdings
    with open('holdings.json', 'r', encoding='utf-8') as h:
        holdings = json.load(h)
        tickers.update(list(holdings['Crypto'].keys()))
        tickers.update(list(holdings['Stocks'].keys()))
        tickers.update(list(holdings['Retirement'].keys()))

    #get tickers from sector experiment
    with open('sector_experiment.json', 'r', encoding='utf-8') as se:
        sector_experiment = json.load(se)
        tickers.update(sector_experiment['Indices'])
        for industry in sector_experiment['Industries'].keys():
            tickers.update(sector_experiment['Industries'][industry]['Tickers'])
            tickers.add(sector_experiment['Industries'][industry]['Comparison'])

    #get tickers from watchlist
    with open('watchlist.json', 'r', encoding='utf-8') as w:
        watchlist = json.load(w)
        tickers.update(watchlist['Tickers'])
    
    return tickers