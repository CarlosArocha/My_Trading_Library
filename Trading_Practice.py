import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt

# Alpha Vantage API Functions:
APIKEY = '7CFUAQQUK36OOGM8'
FilePathOrigin = '/Volumes/OutSSD/DATA/stocks/'

def get_Filepath(*args):

    filepath = FilePathOrigin+args[0]
    for a in args[1:-1]:
        filepath += "-"+a
    return filepath+'.'+args[-1]


def get_Intraday2m(symbol, interval, adjusted='True', outputsize='compact',\
                   apikey=APIKEY):
    '''
    This function returns intraday time series of the equity specified, covering
    extended trading hours where applicable (e.g., 4:00am to 8:00pm Eastern Time
    for the US market). The intraday data is computed directly from the
    Securities Information Processor (SIP) market-aggregated data feed. You can
    query both raw (as-traded) and split/dividend-adjusted intraday data from
    this endpoint.

    This function returns the most recent 1-2 months of intraday data and is best
    suited for short-term/medium-term charting and trading strategy development.
    If you are targeting a deeper intraday history, please use the Extended
    Intraday API.

    Function Parameters:

    ❚ Required: symbol: The name of the equity of your choice. Example: 'IBM'

    ❚ Required: interval: '1min', '5min', '15min', '30min', '60min'

    ❚ Optional: adjusted: True or False

    ❚ Optional: outputsize:
                outputsize=compact (default), returns only the latest 100 data
                points in the intraday time series;
                outputsize=full, returns the full-length intraday time series.

    ❚ Required: apikey

    Returns:
        A Dataframe with columns: timestamp, open, high, low, close, volume
        The filepath option for saving purpose
    '''
    Function = 'TIME_SERIES_INTRADAY'
    Datatype = 'csv'
    url = 'https://www.alphavantage.co/query?function='+Function+              \
                                            '&symbol='+symbol+                 \
                                            '&interval='+interval+             \
                                            '&apikey='+apikey+                 \
                                            '&datatype='+Datatype+             \
                                            '&adjusted='+adjusted+             \
                                            '&outputsize='+outputsize

    filepath = get_Filepath(symbol, 'INTRADAY', interval,\
                            'ADJ' if adjusted else 'RAW',\
                            'SHORT' if outputsize=='compact' else 'FULL',\
                            Datatype)

    return pd.read_csv(url), filepath


def get_Intraday24m(symbol, interval, slice, adjusted='True', apikey=APIKEY):
    '''
    This function returns historical intraday time series for the trailing 2
    years, covering over 2 million data points per ticker. The intraday data is
    computed directly from the Securities Information Processor (SIP) market-
    aggregated data feed. You can query both raw (as-traded) and split/dividend-
    adjusted intraday data from this endpoint. Common use cases for this API
    include data visualization, trading simulation/backtesting, and machine
    learning and deep learning applications with a longer horizon.

    Function Parameters:

    ❚ Required: symbol: The name of the equity of your choice. Example: 'IBM'

    ❚ Required: interval: '1min', '5min', '15min', '30min', '60min'

    ❚ Required: slice: 'year1month1',...,'year1month12',
                       'year2month1',...,'year2month12'

    ❚ Optional: adjusted: True or False

    ❚ Required: apikey

    Returns:
        A Dataframe with the next columns: time, open, high, low, close, volume
        The filepath option for saving purpose
    '''
    Function = 'TIME_SERIES_INTRADAY_EXTENDED'
    url = 'https://www.alphavantage.co/query?function='+Function+              \
                                            '&symbol='+symbol+                 \
                                            '&interval='+interval+             \
                                            '&slice='+slice+                   \
                                            '&adjusted='+adjusted+             \
                                            '&apikey='+apikey

    filepath = get_Filepath(symbol, 'INTRADAY', interval,\
                            'ADJ' if adjusted else 'RAW',\
                            slice, 'csv')

    return pd.read_csv(url), filepath


def get_DailyRaw(symbol, outputsize='compact', apikey=APIKEY):

    '''
    This function returns raw (as-traded) daily time series (date, daily open,
    daily high, daily low, daily close, daily volume) of the global equity
    specified, covering 20+ years of historical data. If you are also interested
    in split/dividend-adjusted historical data, please use the Daily Adjusted
    API, which covers adjusted close values and historical split and dividend
    events.

    Function Parameters:

    ❚ Required: symbol: The name of the equity of your choice. Example: 'IBM'

    ❚ Optional: outputsize:
                outputsize='compact' (default), returns only the latest 100 data
                points in the daily time series;
                outputsize='full', returns the full-length daiily ts = 20+years.

    ❚ Required: apikey

    Returns:
        A Dataframe with columns: timestamp, open, high, low, close, volume
        The filepath option for saving purpose
    '''
    Function = 'TIME_SERIES_DAILY'
    Datatype = 'csv'
    url = 'https://www.alphavantage.co/query?function='+Function+              \
                                            '&symbol='+symbol+                 \
                                            '&outputsize='+outputsize+         \
                                            '&datatype='+Datatype+             \
                                            '&apikey='+apikey

    filepath = get_Filepath(symbol, 'DAILY', 'RAW', \
                            'SHORT' if outputsize=='compact' else 'FULL', \
                            Datatype)

    return pd.read_csv(url), filepath

def get_DailyAdjusted(symbol, outputsize='compact', apikey=APIKEY):

    '''
    This API returns raw (as-traded) daily open/high/low/close/volume values,
    daily adjusted close values, and historical split/dividend events of the
    global equity specified, covering 20+ years of historical data.

    Function Parameters:

    ❚ Required: symbol: The name of the equity of your choice. Example: 'IBM'

    ❚ Optional: outputsize:
                outputsize='compact' (default), returns only the latest 100 data
                points in the daily time series;
                outputsize='full', returns the full-length daiily ts = 20+years.

    ❚ Required: apikey

    Returns:
        A Dataframe with columns: timestamp, open, high, low, close,
                                  adjusted_close, volume, dividend_amount,
                                  and split_coefficient
        The filepath option for saving purpose
    '''
    Function = 'TIME_SERIES_DAILY_ADJUSTED'
    Datatype = 'csv'
    url = 'https://www.alphavantage.co/query?function='+Function+              \
                                            '&symbol='+symbol+                 \
                                            '&outputsize='+outputsize+         \
                                            '&datatype='+Datatype+             \
                                            '&apikey='+apikey

    filepath = get_Filepath(symbol, 'DAILY', 'ADJ', \
                            'SHORT' if outputsize=='compact' else 'FULL', \
                            Datatype)

    return pd.read_csv(url), filepath




#df1, filepath = get_Intraday2m(symbol='AAPL', interval='1min')

#df2, filepath = get_Intraday24m(symbol='AAPL', interval='1min', slice='year1month6')

df3, filepath = get_DailyAdjusted('AAPL', outputsize='full')

#df1.to_csv(filepath, index=False, header=True)
#df1 = pd.read_csv(filepath)
#print(df1, df1.columns, df1.timestamp, df1.close, filepath)

#df2.to_csv(filepath, index=False, header=True)
#df2 = pd.read_csv(filepath)
#print(df2, df2.columns, df2.close, filepath)

df3.to_csv(filepath, index=False, header=True)
df3 = pd.read_csv(filepath)
print(df3, df3.columns, df3.close, filepath)


fig, ax = plt.subplots(figsize=(12,4))
x = df3.sort_values(by='timestamp').timestamp
y = df3.sort_values(by='timestamp')['adjusted_close']
lines = ax.plot(x,y)
plt.show()
