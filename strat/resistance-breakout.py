# -*- coding: utf-8 -*-
"""
Created on Sun May 16 14:58:15 2021

@author: blackmagic
"""

import yfinance as yf

data = yf.download('INFY.BO', period='1mo', interval='5m')

data['roll_max_cp'] = data['High'].rolling(20).max()
