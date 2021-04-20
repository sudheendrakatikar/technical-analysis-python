# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 11:54:19 2021

@author: blackmagic
"""

import yfinance as yf
from datetime import datetime, timedelta

end = datetime.today().strftime('%Y-%m-%d')
start = (datetime.today() - timedelta(360)).strftime('%Y-%m-%d')
data = yf.download('^NSEI', start, end)
