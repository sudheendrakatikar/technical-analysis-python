# -*- coding: utf-8 -*-
"""
Systematic trade generator that chooses
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta

historical = pd.read_csv('S:\\Projects\\algo-trading\\data\\sp500_2010-2019.csv')
sp500 = []
for index, row in historical.iterrows():
    sp500 += historical.iloc[index]['tickers'].split(',')
sp500 = list(set(sp500))
tradeable = pd.read_csv('S:\\Projects\\algo-trading\\data\\tradeable_20210513.csv')['symbol'].tolist()
universe = [ stock for stock in sp500 if stock in tradeable ]

# Dow Jones constituents from 2014
# universe = ["MMM","AXP","T","BA","CAT","CSCO","KO", "XOM","GE","GS","HD",
#             "IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","NKE","PFE","PG","TRV",
#             "UNH","VZ","V","WMT","DIS"]

start = date(2009, 12, 1)
end = date(2019, 12, 31)
data = {}
for stock in universe:
    data[stock] = yf.download(stock, start, end, interval='1mo')
    data[stock].dropna(inplace=True,how="all")

monthly_return = pd.DataFrame()
for stock in universe:
    data[stock]['monthly_ret'] = data[stock]['Close'].pct_change()
    monthly_return[stock] = data[stock]['monthly_ret']
monthly_return.dropna(axis=0,inplace=True,how="all")
monthly_return.dropna(axis=1,inplace=True,how="all")

def strategy(start, end, monthly_return, number, replace):
    portfolio = []
    returns = [ 0 ]
    report = open('S:\\Projects\\algo-trading\\reports\\monthly_rebal.txt', 'w')
    while start <= end:
        today = str(start)
        # report.write('Today is '+today+'\n')
        if len(portfolio) > 0:
            returns.append(monthly_return[portfolio].loc[today].mean())
            bottom = monthly_return[portfolio].loc[today].sort_values(ascending=True)[:replace].index.values.tolist()
            report.write('SELL\n')
            report.write(str(bottom)+'\n')
            for b in bottom:
                report.write(b+'@'+str(round(data[b].loc[today, 'Close'], 2))+'\n')
            portfolio = [ p for p in portfolio if p not in bottom ]
        fill = number - len(portfolio)
        top = monthly_return.drop(portfolio, axis=1).loc[today].sort_values(ascending=False)[:fill].index.values.tolist()
        report.write('BUY\n')
        report.write(str(top)+'\n')
        for t in top:
            report.write(t+'@'+str(round(data[t].loc[today, 'Close'], 2))+'\n')
        portfolio += top
        report.write('Portolio => '+str(portfolio)+'\n')
        start += relativedelta(months=+1)
    report.close()
    return pd.DataFrame(np.array(returns),columns=['mon_ret'])

def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df['cum_return'] = (1 + df['mon_ret']).cumprod()
    n = len(df)/12
    CAGR = (df['cum_return'].tolist()[-1])**(1/n) - 1
    return CAGR


start = date(2010, 1, 1)
end = date(2019, 12, 31)

index = yf.download('^GSPC', start, end, interval='1mo')
index['mon_ret'] = index['Close'].pct_change().fillna(0)
index_return = CAGR(index)
my_return_df = strategy(start, end, monthly_return, 6, 3)
my_return = CAGR(my_return_df)










