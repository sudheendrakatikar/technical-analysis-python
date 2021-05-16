# -*- coding: utf-8 -*-
"""
On Balance Volume - If volume goes up, price is expected to go up
OBV = OBV_prev + (direction*volume)
direction = 1 -> close >= close_prev, else -1
"""

from datetime import datetime, timedelta
import yfinance as yf
import numpy as np

stock = 'TSLA'
end = datetime.today().strftime('%Y-%m-%d')
start = (datetime.today() - timedelta(360)).strftime('%Y-%m-%d')
data = yf.download(stock, start, end)

data['pct_change'] = data['Close'].pct_change()
data['direction'] = np.where(data['pct_change']>=0, 1, -1)
data['direction'][0] = 0
data['vol*dir'] = data['Volume']*data['direction']
data['obv'] = data['vol*dir'].cumsum()