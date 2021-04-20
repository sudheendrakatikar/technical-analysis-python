# -*- coding: utf-8 -*-
"""
Moving Average Convergence Divergence
"""

import yfinance as yf
from datetime import datetime, timedelta

stock = 'TSLA'
end = datetime.today().strftime('%Y-%m-%d')
start = (datetime.today() - timedelta(360)).strftime('%Y-%m-%d')
data = yf.download(stock, start, end)

fast = 12
slow = 26
signal = 9
data['fast'] = data['Close'].ewm(fast).mean()
data['slow'] = data['Close'].ewm(slow).mean()
data['macd'] = data['fast'] - data['slow']
data['signal'] = data['macd'].ewm(signal).mean()

data['macd'].plot(color='black', title='MACD: '+stock)
data['signal'].plot(color='red')