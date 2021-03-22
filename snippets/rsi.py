# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 21:46:15 2021

@author: blackmagic
"""

from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import numpy as np

stock = 'MSFT'
end = datetime.today().strftime('%Y-%m-%d')
start = (datetime.today() - timedelta(60)).strftime('%Y-%m-%d')
t = 14

data = yf.download(stock, start, end)

data['delta'] = data['Close'] - data['Close'].shift(1)
data['gain'] = np.where(data['delta']>0, data['delta'], 0)
data['loss'] = np.where(data['delta']<0, abs(data['delta']), 0)
data.drop(['Volume', 'delta'], axis=1, inplace=True)

avg_gain = []
avg_loss = []

for i in range(len(data)):
    if i < t:
        avg_gain.append(0)
        avg_loss.append(0)
    elif i == t:
        avg_gain.append(data['gain'].rolling(t).mean().tolist()[t])
        avg_loss.append(data['loss'].rolling(t).mean().tolist()[t])
    else:
        avg_gain.append((avg_gain[i-1]*(t-1)+data['gain'][i])/t)
        avg_loss.append((avg_loss[i-1]*(t-1)+data['loss'][i])/t)
        
data['avg_gain'] = np.array(avg_gain)
data['avg_loss'] = np.array(avg_loss)
data['rs'] = data['avg_gain']/data['avg_loss']
data['rsi'] = 100 - 100/(1+data['rs'])


data['rsi'].plot(title='RSI: MSFT')