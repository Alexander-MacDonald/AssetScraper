import datetime

HISTORICALDATAPATH = "historical_data"
METRICDATAPATH = "metric_data"
ERRORPATH = "errors"
RECOLLECTHISTORICALDATA = False
HISOTRYQUERYURL = "https://finance.yahoo.com/quote/{ticker}/history"
LIVEPRICEQUERYURL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1d&interval=2m"
METRICSURL = "https://finviz.com/quote.ashx?t={ticker}&p=d"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}