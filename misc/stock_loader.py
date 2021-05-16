# -*- coding: utf-8 -*-
"""
Gets the list of all tradeable symbols from Financial Modeling Prep
Supported exchanges: NYSE, Nasdaq, NSE, BSE, SEHK
"""

import requests
from tokens import FMP_TOKEN
import pandas as pd
from datetime import datetime

api = 'https://financialmodelingprep.com/api/v3/available-traded/list'
params = { 'datatype': 'csv' , 'apikey': FMP_TOKEN }
response = requests.get(api, params).text

tradeable = 'S:\\Projects\\algo-trading\\data\\tradeable_'+datetime.today().strftime('%Y%m%d')+'.csv'
with open(tradeable, 'w', newline='') as file:
    file.write(response)

master = pd.read_csv(tradeable)


