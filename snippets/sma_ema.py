# -*- coding: utf-8 -*-
"""
Simple/Exponential Moving Average
"""

import yfinance as yf
from datetime import datetime, timedelta

stock = 'TSLA'
end = datetime.today().strftime('%Y-%m-%d')
start = (datetime.today() - timedelta(360)).strftime('%Y-%m-%d')

st = 50
lt = 100

data = yf.download(stock, start, end)
data['st'] = data['Close'].rolling(st).mean()
data['lt'] = data['Close'].rolling(lt).mean()

data['st'].plot()
data['lt'].plot()