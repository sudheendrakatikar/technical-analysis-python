# -*- coding: utf-8 -*-
"""
Williams %R = HighestHigh(t) - Close / HighestHigh(t) - LowestLow(t)
Range    Signal
0-20     SELL
80-100   BUY
"""

import yfinance as yf
from datetime import datetime, timedelta

stock = 'TSLA'
end = datetime.today().strftime('%Y-%m-%d')
start = (datetime.today() - timedelta(360)).strftime('%Y-%m-%d')
t = 14

data = yf.download(stock, start, end)
data['nr'] = data['High'].rolling(t).max() - data['Close']
data['dr'] = data['High'].rolling(t).max() - data['Low'].rolling(t).min()
data['wr'] = data['nr'] / data['dr'] * 100

ax = data['wr'].plot(title='Williams %R: '+stock, ylim=(0,100))
ax.axhline(y=80, color='red', ls=':')
ax.axhline(y=20, color='green', ls=':')