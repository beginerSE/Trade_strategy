# 動作環境　jupyter notebook
import matplotlib.pyplot as plt
%matplotlib inline
import numpy as np
import time
import requests
import json
from datetime import datetime
import pandas as pd

# coingeckoのAPIからビットコインの価格データを取得する関数
def get_btcprice(ticker, max):
    url = 'https://api.coingecko.com/api/v3/coins/' + ticker + '/market_chart?vs_currency=jpy&days=' + max
    r = requests.get(url)
    r2 = json.loads(r.text)
    return r2

#jsonから価格データだけをPandasに変換して抽出する
def get_price(r2):
    data = pd.DataFrame(r2['prices'])
    data.columns = ['date','price']
    date = []
    for i in data['date']:
        tsdate = int(i / 1000)
        loc = datetime.utcfromtimestamp(tsdate)
        date.append(loc)
    data.index = date
    del data['date']
    return data

#ビットコインの全期間の価格データを取得する
r2 = get_btcprice('bitcoin', 'max')
btc = get_price(r2)
price = btc['price']
