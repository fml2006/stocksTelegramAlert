import yfinance as yf
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy import update
import numpy as np

def connectDB():
    dataCon = 'mysql+pymysql://root:@localhost/market_stocks'
    return create_engine(dataCon)

def getDataFromYF(ticker, timeFrame, uploadTime):
    data = yf.download(  
            tickers = ticker,
            period = uploadTime,
            interval = timeFrame,
            group_by = 'ticker',
            auto_adjust = True,
            prepost = False,
            threads = True,
            proxy = None
        )
    data['Date'] = data.index.strftime('%Y-%m-%d')
    #EN HORARIO DE RUEDA DESCOMENTAR ESTA LINEA PARA ACTUALIZAR EN TIEMPO REAL LOS VALORES. 
    #data.drop(data.tail(1).index,inplace=True)
    return data

def checkExistTablet(dbName, tableName):
    con = connectDB()
    query = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{1}' AND table_name = '{2}'".format(tableName, dbName, tableName)
    query = con.execute(query)
    result = query.fetchone()
    tableExist = result[0]
    if tableExist:
        return True
    else:
        return False

def addDataToDB(data, tableName):
    con = connectDB()
    data.to_sql(name=tableName, con=con, if_exists='append')
    query = 'ALTER TABLE ' + tableName + ' ADD COLUMN CCI VARCHAR(20), ADD COLUMN VolMean VARCHAR(20) AFTER Date'
    query = con.execute(query)

def getLastUploadDB(tableName):
    con = connectDB()
    data = con.execute('SELECT * FROM ' + tableName + ' ORDER BY Datetime DESC LIMIT 1')
    data = data.fetchone()
    dataLastDate = data['Date']
    return dataLastDate

def deleteLastRows(tableName, dayRow):
    con = connectDB()
    query = "DELETE FROM {0} WHERE Date = '{1}'".format(tableName, dayRow)
    query = con.execute(query)

def addDateData(tableName, data):
    con = connectDB()
    VolMean = "Sin Calculo"
    CCI = "Sin Calculo"
    for i in range(len(data)):
        query = "INSERT INTO {0} (Datetime, Open, High, Low, Close, Volume, `Date`, VolMean, CCI) VALUES ('{1}' , {2} , {3} , {4} , {5} , {6}, '{7}', '{8}', '{9}')".format(str(tableName), str(data.index[i].strftime('%Y-%m-%d %H:%M:%S')), str(data.Open[i]), str(data.High[i]), str(data.Low[i]), str(data.Close[i]), str(data.Volume[i]), str(data.Date[i]), VolMean, CCI)
        query = con.execute(query)

def updateData(data, tableName, indicator):
    con = connectDB()
    for i in range(len(data)):
        query = "UPDATE {0} SET {1} = '{2}' WHERE Datetime = '{3}'".format(str(tableName), indicator, data[indicator][i], data.Datetime[i])
        query = con.execute(query)
    
def getDataFromDB(tableName):
    con = connectDB()
    data = pd.read_sql(tableName, con)
    return data

def CCI(data, ndays):
    TP = (data['High'] + data['Low'] + data['Close']) / 3 
    data['CCI'] = (TP - TP.rolling(ndays).mean()) / (0.015 * TP.rolling(ndays).std())
    return data

def volMean(data, ndays):
    data['VolMean'] = data['Volume'].rolling(ndays).mean()
    return data

def addIndicators(tableName):
    data = getDataFromDB(tableName)
    data = CCI(data, 20)
    data = volMean(data, 20)
    updateData(data, tableName, 'CCI')
    updateData(data, tableName, 'VolMean')

def sendAlert(data, ticker):
    print(ticker.upper())
    return ticker.upper()

def dataStock(ticker, tableName):
    con = connectDB()
    data = con.execute('SELECT * FROM ' + tableName + ' ORDER BY Datetime DESC LIMIT 1')
    data = data.fetchone()
    return data

def analyzeStock(ticker, tableName):
    con = connectDB()
    data = con.execute('SELECT * FROM ' + tableName + ' ORDER BY Datetime DESC LIMIT 1')
    data = data.fetchone()
    CCI = float(data['CCI'])
    if CCI <= 30:
        return ticker

def initScreener(ticker, timeFrame, uploadTwoYearsAgo, uploadLastDay, tableName, dbName):
    checkDB = checkExistTablet(dbName, tableName)
    if checkDB:
        #ACTUALIZO DATA
        data = getDataFromYF(ticker, timeFrame, uploadLastDay)
        dateLastUpload = getLastUploadDB(tableName)
        dateNewData = data['Date'].iloc[-1]
        if dateLastUpload != dateNewData:
            addDateData(tableName, data)
            #Inicio del dia Agrego nueva Data"
        elif dateLastUpload == dateNewData:
            deleteLastRows(tableName, dateLastUpload)
            addDateData(tableName, data)
            #Actualizo Data del dia
        else:
            print("HAY ERRORES")
            #HAY ALGUN TIPO DE ERROR
    else:
        print("Creo y Guardo DATA")
        data = getDataFromYF(ticker, timeFrame, uploadTwoYearsAgo)
        addDataToDB(data, tableName)
    addIndicators(tableName)
    stocksAlert = np.array([])
    stockAlertTicker = analyzeStock(ticker, tableName)
    if stockAlertTicker:
        stocksAlert = np.append(stocksAlert, stockAlertTicker)
    return stocksAlert    
    

