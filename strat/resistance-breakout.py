# -*- coding: utf-8 -*-
"""
Created on Sun May 16 14:58:15 2021

@author: blackmagic
"""

import yfinance as yf
import pandas as pd
import date

universe = pd.read_csv('S:\\Projects\\algo-trading\\data\\sensex_historical.csv')['Symbol'].tolist()
start = date(2019, 1, 1)
end = date(2019, 12, 31)
data = [ yf.download(stock, period='1mo', interval='5m') for stock in universe ]

data['roll_max_cp'] = data['High'].rolling(20).max()
