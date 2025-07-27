import os
import csv
import requests
from bs4 import BeautifulSoup

import CFG

def getMetrics(tickers):
    #make metrics folder
    try:
        os.makedirs(CFG.METRICDATAPATH, exist_ok=True)
    except OSError as e:
        print(f"Error creating folder: {e}", flush=True)
    
    #csv file per stock storing x data from finviz
    for ticker in tickers:
        try:
            os.makedirs(CFG.METRICDATAPATH + "/" + ticker, exist_ok=True)
        except OSError as e:
            print(f"Error creating folder: {e}", flush=True)
        if os.path.exists(CFG.METRICDATAPATH + "/" + ticker + "/" + ticker + ".csv"):
            print("Metric Data for " + ticker + " found... checking last get", flush=True)
            #getTickerMetrics(ticker)
            continue
        #otherwise...
        with open(CFG.HISTORICALDATAPATH + "/" + ticker + "/" + ticker + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date","P/E","Market Cap","EPS(ttm)","Debt/Eq","Dividend"])
        getTickerMetrics(ticker)

def getTickerMetrics(ticker):
    req = requests.get(CFG.METRICSURL.format(ticker=ticker), headers=CFG.HEADERS)
    htmlParser = BeautifulSoup(req.text, 'html.parser')
    table = htmlParser.select_one('table.js-snapshot-table.snapshot-table2.screener_snapshot-table-body')
    if table:
        rows = []
        for row in table.find_all('tr'):
            cols = []
            for col in row.find_all(['td', 'th']):
                text_parts = list(col.stripped_strings)
                cols.append(' '.join(text_parts))
            rows.append(cols)
        with open(CFG.HISTORICALDATAPATH + "/" + ticker + "/" + ticker + ".csv", "a", newline="") as f:
            writer = csv.writer(f)
            #add cols to csv