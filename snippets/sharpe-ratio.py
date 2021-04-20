# -*- coding: utf-8 -*-
"""
Sharpe Ratio for comparing performace of NIFTY with GOI 10Y Bond
S(x) = [ R(x) - Rf ] / V(x)
"""

import yfinance as yf
import numpy as np

Rf = 0.07695            # 10-Year GOI Bond Yield as on Jan 1, 2010
n = 10
stock = '^NSEI'
start = '2010-01-01'
end = '2019-12-31'
data = yf.download(stock, start, end)

def cagr(data, n):
    return (data[-1]/data[0]) ** (1/n) - 1

def volatility(data):
    return data.pct_change().std() * np.sqrt(252)

Rx = cagr(data['Close'], n)
Vx = volatility(data['Close'])

Sx = (Rx - Rf)/Vx