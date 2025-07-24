import os
import json
import time
import shutil

import seleniumHandler
import tickerAggregator
import CFG

try:
    os.makedirs(CFG.HISTORICALDATAPATH, exist_ok=True)
except OSError as e:
    print(f"Error creating folder: {e}", flush=True)
    
try:
    os.makedirs(CFG.ERRORPATH, exist_ok=True)
except OSError as e:
    print(f"Error creating folder: {e}", flush=True)

tickers = tickerAggregator.getTickers()

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
    print("Ratelimit Waiting...", flush=True)
    time.sleep(5)
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
            #add checking date logic
        else:
            #no meta file, delete the csv and start
            pass
    else:
        seleniumHandler.fetchRetry(ticker)
        



    
    
#for each ticker, get all close data since 1970
#if ticker folder doesn't exist, make it
    #if ticker.csv doesn't exist, make it
    #if it does exist
        #if meta file exists, check if meta date is before yesterday
        #if before yesterday, get info from last update to today & append to csv file
        #if meta file doesn't exist
            #delete ticker.csv & restart collection
    #when done, make or edit meta file that denotes:
        #last close recorded