import os
import time
import csv
import json
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import CFG

def writeMeta(ticker):
    data = {
        "last_collected": str(date.today())
    }

    with open(CFG.HISTORICALDATAPATH + "/" + ticker + "/meta.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    print("meta.json created with today's date for: " + ticker, flush=True)

def extractData(driver, ticker, ldc):
    rows = driver.find_elements(By.CSS_SELECTOR, "div.table-container table tbody tr")
    if(not os.path.exists(CFG.HISTORICALDATAPATH + "/" + ticker + "/" + ticker + ".csv")):
        with open(CFG.HISTORICALDATAPATH + "/" + ticker + "/" + ticker + ".csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date","Open","High","Low","Close"])

    with open(CFG.HISTORICALDATAPATH + "/" + ticker + "/" + ticker + ".csv", "a", newline="") as f:
        writer = csv.writer(f)
        print(f"Writing CSV Data for: {ticker}", flush=True)
        tmpYear = 0
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 6:
                continue
            date = cols[0].text.strip()
            if(date > ldc):
                if(int(date[-4:]) != tmpYear):
                    tmpYear = int(date[-4:])
                    print(ticker + ": " + str(tmpYear), flush=True)
                o = cols[1].text.strip()
                high = cols[2].text.strip()
                low = cols[3].text.strip()
                close = cols[4].text.strip()
                writer.writerow([date, o, high, low, close])
            else:
                break
        print(f"Finished writing CSV data for {ticker}", flush=True)
        writeMeta(ticker)


def fetchData(ticker, maxPress=False, date=""):
    print("Ratelimit Waiting...", flush=True)
    time.sleep(5)
    driverOptions = Options()
    driverOptions.add_argument("--headless=new")
    driverOptions.add_argument("--disable-gpu")
    driverOptions.add_argument("--window-size=1920,1080")
    driverOptions.add_argument("--incognito")

    chromeDriver = webdriver.Chrome(service=Service(), options=driverOptions)

    try:
        chromeDriver.get(CFG.HISOTRYQUERYURL.format(ticker=ticker))

        # Handle Cookies
        try:
            cookies = WebDriverWait(chromeDriver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Accept all']]"))
            )
            cookies.click()
            time.sleep(5)
        except:
            pass
        if(maxPress):
            # Data range toolbar
            WebDriverWait(chromeDriver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='history-toolbar']"))
            )

            # Date Range Button
            date_button = WebDriverWait(chromeDriver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='history-toolbar'] button"))
            )
            date_button.click()

            # Click Max Range
            max_button = WebDriverWait(chromeDriver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[value='MAX']"))
            )
            max_button.click()

            #Table can take a LONG time to load
            time.sleep(50)

        extractData(chromeDriver, ticker, date)
    except Exception as e:
        print(f"Exception occurred:", repr(e), flush=True)
        chromeDriver.save_screenshot(CFG.ERRORPATH + f"/" + str(time.time_ns()) + f"{ticker}-error.png")
        with open(CFG.ERRORPATH + f"/" + str(time.time_ns()) + f"{ticker}-page_source.html", "w", encoding="utf-8") as f:
            f.write(chromeDriver.page_source)
    finally:
        chromeDriver.quit()


def totalFetchRetry(ticker):
    for attempt in range(1, 11):
        print(f"Attempt {attempt} of 10 for {ticker}", flush=True)
        try:
            fetchData(ticker, True)
            print(f"Fetch {attempt} for {ticker} successful!", flush=True)
            break
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}", flush=True)
            time.sleep(5)
    else:
        print(f"All attempts failed for ticker: {ticker}", flush=True)

def finiteFetchRetry(ticker, date):
    for attempt in range(1, 11):
        print(f"Attempt {attempt} of 10 for {ticker}", flush=True)
        try:
            fetchData(ticker, False, date)
            print(f"Fetch {attempt} for {ticker} successful!", flush=True)
            break
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}", flush=True)
            time.sleep(5)
    else:
        print(f"All attempts failed for ticker: {ticker}", flush=True)