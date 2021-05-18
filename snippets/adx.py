# -*- coding: utf-8 -*-
"""
Average Directional Index
Range    Strength
0-25     Absent/Weak
25-50    Strong
50-75    Very strong
75-100   Extremely strong
"""

import yfinance as yf
import numpy as np
from datetime import date

stock = 'TSLA'
start = date(2020, 4, 2)
end = date(2021, 4, 1)
data = yf.download(stock, start, end)
n = 14

data['true_high'] = np.where(data['High'] >= data['Close'].shift(1), data['High'], data['Close'].shift(1))
data['true_low'] = np.where(data['Low'] <= data['Close'].shift(1), data['Low'], data['Close'].shift(1))
data['true_range'] = data['true_high'] - data['true_low']

data['delta_high'] = data['High'].shift(1) - data['High']
data['delta_low'] = data['Low'] - data['Low'].shift(1)
data['DM+'] = np.where(data['delta_high'] >= data['delta_low'], data['delta_high'], 0)
data['DM+'] = np.where(data['DM+'] >0, data['DM+'], 0)
data['DM-'] = np.where(data['delta_low'] > data['delta_high'], data['delta_low'], 0)
data['DM-'] = np.where(data['DM-'] >0, data['DM-'], 0)

tr = []
dmp = []
dmm = []
for i in range(len(data)):
    if i < n:
        tr.append(0)
        dmp.append(0)
        dmm.append(0)
    elif i == n:
        tr.append(sum(data[1:n+1]['true_range']))
        dmp.append(sum(data[1:n+1]['DM+']))
        dmm.append(sum(data[1:n+1]['DM-']))
    else:
        tr.append(tr[i-1] - tr[i-1]/n + data.iloc[i]['true_range'])
        dmp.append(dmp[i-1] - dmp[i-1]/n + data.iloc[i]['DM+'])
        dmm.append(dmm[i-1] - dmm[i-1]/n + data.iloc[i]['DM-'])
data['TR14'] = np.array(tr)
data['DM+14'] = np.array(dmp)
data['DM-14'] = np.array(dmm)
data['DI+'] = data['DM+14']/data['TR14'] * 100
data['DI-'] = data['DM-14']/data['TR14'] * 100
data['DX'] = abs((data['DI+']-data['DI-']) / (data['DI+']+data['DI-'])) * 100

adx = []
for i in range(len(data)):
    if i < 2*n-1:
        adx.append(0)
    elif i == 2*n-1:
        adx.append(sum(data[n:2*n]['DX']) / n)
    else:
        adx.append((adx[i-1]*(n-1) + data.iloc[i]['DX']) / n)
data['ADX'] = np.array(adx)

ax = data['ADX'].plot(title='ADX: '+stock, ylim=(0,100))
ax.axhline(y=25, color='red', ls=':')
ax.axhline(y=50, color='orange', ls=':')
ax.axhline(y=75, color='green', ls=':')