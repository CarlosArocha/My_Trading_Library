import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt

# INITIAL CONFIGURATION
pd.set_option('display.max_columns', None)
APIKEY = '7CFUAQQUK36OOGM8'
FilePathOrigin = '/Volumes/OutSSD/DATA/stocks/'

def get_Filepath(*args):

    filepath = FilePathOrigin+args[0]
    for a in args[1:-1]:
        filepath += "-"+a
    return filepath+'.'+args[-1]

################################################################################
##                                                                            ##
##              Alpha Vantage API Functions: STOCKS TIME SERIES               ##
##                                                                            ##
################################################################################

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

    * Required: symbol: The name of the equity of your choice. Example: 'IBM'

    * Required: interval: '1min', '5min', '15min', '30min', '60min'

    * Optional: adjusted: True or False

    * Optional: outputsize:
                outputsize=compact (default), returns only the latest 100 data
                points in the intraday time series;
                outputsize=full, returns the full-length intraday time series.

    * Required: apikey

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

    * Required: symbol: The name of the equity of your choice. Example: 'IBM'

    * Required: interval: '1min', '5min', '15min', '30min', '60min'

    * Required: slice: 'year1month1',...,'year1month12',
                       'year2month1',...,'year2month12'

    * Optional: adjusted: True or False

    * Required: apikey

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

    * Required: symbol: The name of the equity of your choice. Example: 'IBM'

    * Optional: outputsize:
                outputsize='compact' (default), returns only the latest 100 data
                points in the daily time series;
                outputsize='full', returns the full-length daiily ts = 20+years.

    * Required: apikey

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
    This function returns raw (as-traded) daily open/high/low/close/volume
    values, daily adjusted close values, and historical split/dividend events of
    the global equity specified, covering 20+ years of historical data.

    Function Parameters:

    * Required: symbol: The name of the equity of your choice. Example: 'IBM'

    * Optional: outputsize:
                outputsize='compact' (default), returns only the latest 100 data
                points in the daily time series;
                outputsize='full', returns the full-length daiily ts = 20+years.

    * Required: apikey

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

def get_WeeklyRaw(symbol, apikey=APIKEY):

    '''
    This function returns weekly time series (last trading day of each week,
    weekly open, weekly high, weekly low, weekly close, weekly volume) of the
    global equity specified, covering 20+ years of historical data.

    Function Parameters:

    * Required: symbol: The name of the equity of your choice. Example: 'IBM'

    * Required: apikey

    Returns:
        A Dataframe with columns: timestamp, open, high, low, close, volume
        The filepath option for saving purpose
    '''
    Function = 'TIME_SERIES_WEEKLY'
    Datatype = 'csv'
    url = 'https://www.alphavantage.co/query?function='+Function+              \
                                            '&symbol='+symbol+                 \
                                            '&datatype='+Datatype+             \
                                            '&apikey='+apikey

    filepath = get_Filepath(symbol, 'WEEKLY', 'RAW', \
                            Datatype)

    return pd.read_csv(url), filepath

def get_WeeklyAdjusted(symbol, apikey=APIKEY):

    '''
    This function returns weekly adjusted time series (last trading day of each
    week, weekly open, weekly high, weekly low, weekly close, weekly adjusted
    close, weekly volume, weekly dividend) of the global equity specified,
    covering 20+ years of historical data.

    Function Parameters:

    * Required: symbol: The name of the equity of your choice. Example: 'IBM'

    * Required: apikey

    Returns:
        A Dataframe with columns: timestamp, open, high, low, close,
                                  adjusted close, volume
        The filepath option for saving purpose
    '''
    Function = 'TIME_SERIES_WEEKLY_ADJUSTED'
    Datatype = 'csv'
    url = 'https://www.alphavantage.co/query?function='+Function+              \
                                            '&symbol='+symbol+                 \
                                            '&datatype='+Datatype+             \
                                            '&apikey='+apikey

    filepath = get_Filepath(symbol, 'WEEKLY', 'ADJ', \
                            Datatype)

    return pd.read_csv(url), filepath

def get_MonthlyRaw(symbol, apikey=APIKEY):

    '''
    This function returns monthly time series (last trading day of each month,
    monthly open, monthly high, monthly low, monthly close, monthly volume) of
    the global equity specified, covering 20+ years of historical data.

    Function Parameters:

    * Required: symbol: The name of the equity of your choice. Example: 'IBM'

    * Required: apikey

    Returns:
        A Dataframe with columns: timestamp, open, high, low, close, volume
        The filepath option for saving purpose
    '''
    Function = 'TIME_SERIES_MONTHLY'
    Datatype = 'csv'
    url = 'https://www.alphavantage.co/query?function='+Function+              \
                                            '&symbol='+symbol+                 \
                                            '&datatype='+Datatype+             \
                                            '&apikey='+apikey

    filepath = get_Filepath(symbol, 'MONTHLY', 'RAW', \
                            Datatype)

    return pd.read_csv(url), filepath

def get_Quote(symbol, apikey=APIKEY):

    '''
    A lightweight alternative to the time series functions, this service returns
    the price and volume information for a security of your choice.

    Function Parameters:

    * Required: symbol: The name of the equity of your choice. Example: 'IBM'

    * Required: apikey

    Returns:
        A Dataframe with columns: symbol, open, high, low, price, volume,
                                  latestDay, previousClose, change,
                                  changePercent
    '''
    Function = 'GLOBAL_QUOTE'
    Datatype = 'csv'
    url = 'https://www.alphavantage.co/query?function='+Function+              \
                                            '&symbol='+symbol+                 \
                                            '&datatype='+Datatype+             \
                                            '&apikey='+apikey

    return pd.read_csv(url)

def get_SearchTicker(text, apikey=APIKEY):

    '''
    We've got you covered! The Search Endpoint returns the best-matching symbols
    and market information based on keywords of your choice. The search results
    also contain match scores that provide you with the full flexibility to
    develop your own search and filtering logic.

    Function Parameters:

    * Required: text: A text string of your choice. For example: 'microsoft.'

    * Required: apikey

    Returns:
        A Dataframe with columns: symbol, name, type, region, marketOpen,
                                  marketClose, timezone, currency, matchScore
    '''
    Function = 'SYMBOL_SEARCH'
    Datatype = 'csv'
    url = 'https://www.alphavantage.co/query?function='+Function+              \
                                            '&keywords='+text+                 \
                                            '&datatype='+Datatype+             \
                                            '&apikey='+apikey

    return pd.read_csv(url)

################################################################################
##                                                                            ##
##              Alpha Vantage API Functions: FUNDAMENTALS                     ##
##                                                                            ##
################################################################################

def get_CompanyOverview(symbol, apikey=APIKEY):

    '''
    This function returns the company information, financial ratios, and other
    key metrics for the equity specified. Data is generally refreshed on the
    same day a company reports its latest earnings and financials.

    Function Parameters:

    * Required: symbol: The name of the equity of your choice. Example: 'IBM'

    * Required: apikey

    Returns:
        A Dataframe with columns: 'Symbol', 'AssetType', 'Name', 'Description',
                                  'Exchange', 'Currency','Country', 'Sector',
                                  'Industry', 'Address', 'FullTimeEmployees',
                                  'FiscalYearEnd', 'LatestQuarter',
                                  'MarketCapitalization', 'EBITDA','PERatio',
                                  'PEGRatio', 'BookValue', 'DividendPerShare',
                                  'DividendYield','EPS', 'RevenuePerShareTTM',
                                  'ProfitMargin', 'OperatingMarginTTM',
                                  'ReturnOnAssetsTTM', 'ReturnOnEquityTTM',
                                  'RevenueTTM','GrossProfitTTM','DilutedEPSTTM',
                                  'QuarterlyEarningsGrowthYOY',
                                  'QuarterlyRevenueGrowthYOY',
                                  'AnalystTargetPrice','TrailingPE','ForwardPE',
                                  'PriceToSalesRatioTTM', 'PriceToBookRatio',
                                  'EVToRevenue','EVToEBITDA', 'Beta',
                                  '52WeekHigh','52WeekLow','50DayMovingAverage',
                                  '200DayMovingAverage', 'SharesOutstanding',
                                  'SharesFloat','SharesShort',
                                  'SharesShortPriorMonth', 'ShortRatio',
                                  'ShortPercentOutstanding','ShortPercentFloat',
                                  'PercentInsiders','PercentInstitutions',
                                  'ForwardAnnualDividendRate',
                                  'ForwardAnnualDividendYield', 'PayoutRatio',
                                  'DividendDate','ExDividendDate',
                                  'LastSplitFactor', 'LastSplitDate'],
    '''
    Function = 'OVERVIEW'
    url = 'https://www.alphavantage.co/query?function='+Function+              \
                                            '&symbol='+symbol+                 \
                                            '&apikey='+apikey

    #return pd.read_json(url, orient='records')
    return pd.DataFrame(requests.get(url).json(), index=[0])

def get_CompanyEarnings(symbol, apikey=APIKEY):

    '''
    This function returns the annual and quarterly earnings (EPS) for the
    company of interest. Quarterly data also includes analyst estimates and
    surprise metrics.

    Function Parameters:

    * Required: symbol: The name of the equity of your choice. Example: 'IBM'

    * Required: apikey

    Returns:
        A Dataframe dfYear: With the annual earnings for 20+ years.
                            With the next columns:
                                'fiscalDateEnding' and 'reportedEPS'
        A Dataframe dfQuart: With the quarterly earnings info for 20+ years.
                            With the next columns:
                                'fiscalDateEnding', 'reportedDate',
                                'reportedEPS', 'estimatedEPS', 'surprise' and
                                'surprisePercentage'
    '''
    Function = 'EARNINGS'
    url = 'https://www.alphavantage.co/query?function='+Function+              \
                                            '&symbol='+symbol+                 \
                                            '&apikey='+apikey

    jsonDict =  requests.get(url).json()
    jsonDict.pop('symbol')
    return  pd.DataFrame.from_dict(jsonDict.get('annualEarnings')),\
            pd.DataFrame.from_dict(jsonDict.get('quarterlyEarnings'))




dfa, dfb = get_CompanyEarnings('ba')
print(dfa, '\n', dfb)



'''df, filepath = get_MonthlyAdjusted('AAPL')

df.to_csv(filepath, index=False, header=True)
df = pd.read_csv(filepath)
print(df, df.columns, filepath)


fig, ax = plt.subplots(figsize=(12,4))
x = df.sort_values(by='timestamp').timestamp
y = df.sort_values(by='timestamp')['adjusted close']
lines = ax.plot(x,y)
plt.show()'''
