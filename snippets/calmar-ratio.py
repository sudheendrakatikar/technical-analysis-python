# -*- coding: utf-8 -*-
"""
Calmar Ratio: Measure of return over risk (risk adjusted return)
CR = CAGR / Max_Drawdown
"""

import yfinance as yf

n = 10
stock = '^NSEI'
start = '2010-01-01'
end = '2019-12-31'
data = yf.download(stock, start, end)

def CAGR(data, n):
    return (data[-1]/data[0]) ** (1/n) - 1

def max_drawdown(data):
    data['daily_ret'] = data['Close'].pct_change()
    data['cum_ret'] = (1+data['daily_ret']).cumprod()
    data['cum_max'] = data['cum_ret'].cummax()
    data['drawdown'] = data['cum_max'] - data['cum_ret']
    data['drawdown_pct'] = data['drawdown']/data['cum_max']
    return data['drawdown_pct'].max()
    
def calmar(data, n):
    cagr = CAGR(data['Close'], n)
    max_dd = max_drawdown(data)
    return cagr/max_dd

calmar_ratio = calmar(data, n)
