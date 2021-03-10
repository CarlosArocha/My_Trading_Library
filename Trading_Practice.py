import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt

# Alpha Vantage API Functions:
APIKEY = '7CFUAQQUK36OOGM8'
function = 'TIME_SERIES_INTRADAY'
symbol = 'AAPL'
interval = '1min'
datatype = 'csv'
adjusted = 'True'
outputsize = 'full'
filepath = '/Volumes/OutSSD/DATA/Stocks/AAPL-INTRADAY-60days-20210309.csv'

def AlphaVantageData(function, symbol, interval, datatype='json', apikey=APIKEY,\
                        adjusted='True', outputsize='compact'):

    url = 'https://www.alphavantage.co/query?function='+function+               \
                                            '&symbol='+symbol+                  \
                                            '&interval='+interval+              \
                                            '&apikey='+apikey+                  \
                                            '&datatype='+datatype+              \
                                            '&adjusted='+adjusted+              \
                                            '&outputsize='+outputsize
    if datatype=='json':
        return pd.read_json(url, orient='values')
    else:
        return pd.read_csv(url)

#r = requests.get(url)
df = AlphaVantageData(function=function, symbol=symbol, interval=interval,      \
                        datatype=datatype, adjusted=adjusted,                   \
                        outputsize=outputsize)
#print(r.text)
#df.to_csv(filepath, index=False, header=True)
df2 = pd.read_csv(filepath)

fig, ax = plt.subplots(figsize=(12,4))
x = df2.timestamp
y = df2['close']
lines = ax.plot(x,y)
plt.show()


print(df2, df2.shape, df2.timestamp, df2.close)
