import os
import datetime
import json
import shutil
import pandas as pd

import stockGetters.seleniumHandler as seleniumHandler
import CFG



def findLastDateCollected(ticker):
    data = pd.read_csv(CFG.HISTORICALDATAPATH + "/" + ticker + "/" + ticker + ".csv", parse_dates=["Date"])
    return data['Date'].max().strftime('%b %d, %Y')

def checkHistoricalData(tickers):
    try:
        os.makedirs(CFG.HISTORICALDATAPATH, exist_ok=True)
    except OSError as e:
        print(f"Error creating folder: {e}", flush=True)
        
    try:
        os.makedirs(CFG.ERRORPATH, exist_ok=True)
    except OSError as e:
        print(f"Error creating folder: {e}", flush=True)

    #TODO get tickers from nasdaq
    print("Collecting Data for Tickers: " + str(tickers), flush=True)
    #add full recollection flag

    if(CFG.RECOLLECTHISTORICALDATA):
        print("Resetting Historical Data", flush=True)
        if os.path.exists(CFG.HISTORICALDATAPATH) and os.path.isdir(CFG.HISTORICALDATAPATH):
            shutil.rmtree(CFG.HISTORICALDATAPATH)
            os.makedirs(CFG.HISTORICALDATAPATH)
        else:
            print("Historical data folder doesn't exist... Exiting")
            exit
        
    for ticker in tickers:
        print("Collecting Historical Data for: " + ticker, flush=True)
        tickerPath = CFG.HISTORICALDATAPATH + "/" + ticker
        csvFile = tickerPath + "/" + ticker + ".csv"
        metaFile = tickerPath + "/meta.json"

        try:
            os.makedirs(tickerPath, exist_ok=True)
        except OSError as e:
            print(f"Error creating folder: {e}", flush=True)
            print(f"Skipping '{ticker}'", flush=True)
            continue
        if os.path.exists(csvFile):
            print("CSV file found for ticker: " + ticker, flush=True)
            if os.path.exists(metaFile):
                print("Meta file found for ticker: " + ticker, flush=True)
                with open(metaFile, 'r', encoding='utf-8') as m:
                    meta = json.load(m)
                    if(meta['last_collected'] == str(datetime.date.today())):
                        print("Data already collected for " + ticker + " today\nSkipping " + ticker, flush=True)
                        continue
                print("Data not collected for " + ticker + " today", flush=True)
                lastDateCollected = findLastDateCollected(ticker)
                print("Data last collected on: " + lastDateCollected, flush=True)
                seleniumHandler.finiteFetchRetry(ticker, lastDateCollected)
            else:
                #no meta file, delete the csv and start
                print("No Meta file found for ticker: " + ticker + " recollecting data", flush=True)
                os.remove(csvFile)
                seleniumHandler.totalFetchRetry(ticker)
                pass
        else:
            seleniumHandler.totalFetchRetry(ticker)