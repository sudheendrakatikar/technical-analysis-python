# -*- coding: utf-8 -*-
"""
Bollinger Bands
"""

import yfinance as yf
from datetime import datetime, timedelta

stock = 'TSLA'
end = datetime.today().strftime('%Y-%m-%d')
start = (datetime.today() - timedelta(360)).strftime('%Y-%m-%d')
data = yf.download(stock, start, end)

t = 20
sd = 2
data['upper'] = data['Close'].rolling(t).mean() + sd*data['Close'].rolling(t).std()
data['lower'] = data['Close'].rolling(t).mean() - sd*data['Close'].rolling(t).std()

data['upper'].plot(color='green')
data['lower'].plot(color='red')
data['Close'].plot(color='black', title=str(t)+'-day Bollinger Bands: '+stock)