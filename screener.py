import functions as f
import datetime
import pandas as pd
import numpy as np

def initBot():
    tickers = ['aa', 'aapl', 'ggal', 'jpm', 'bac', 'dal', 'ba', 'amd', 'f', 'axp', 'bbd', 'ccl', 'aig', 'fb', 'jmia']
    dbName = 'market_stocks'
    timeFrame = '60m'
    uploadTwoYearsAgo = '5d'
    uploadLastDay = '1d'
    stocksAlert = np.array([]) 
    for i in range(len(tickers)):
        tableName = tickers[i] + timeFrame
        stocksAlert = np.append(stocksAlert, f.initScreener(tickers[i], timeFrame, uploadTwoYearsAgo, uploadLastDay, tableName, dbName))
    return stocksAlert

def initOneStock(ticker):
    timeFrame = '60m'
    tableName = ticker + timeFrame
    stockAlertTicker = f.dataStock(ticker, tableName)
    return stockAlertTicker 