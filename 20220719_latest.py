import numpy as np
import talib
import pandas as pd
import matplotlib.pyplot as plt
df_2019 = pd.read_csv(r"C:\Users\81903\Desktop\Python関係\システムトレード関連\bf_bitcoin5min.csv")
df_2019

%matplotlib inline
def psar(barsdata, iaf = 0.01, maxaf = 0.2):
    length = len(barsdata)
    dates = barsdata['close_time'].tolist()
    high = barsdata['high_price'].tolist()
    low = barsdata['low_price'].tolist()
    close = barsdata['close_price'].tolist()
    psar = close[0:len(close)]
    psarbull = [None] * length
    psarbear = [None] * length
    bull = True
    af = iaf
    ep = low[0]
    hp = high[0]
    lp = low[0]
    
    for i in range(2,length):
        if bull:
            psar[i] = psar[i - 1] + af * (hp - psar[i - 1])
        else:
            psar[i] = psar[i - 1] + af * (lp - psar[i - 1])
        
        reverse = False
        
        if bull:
            if low[i] < psar[i]:
                bull = False
                reverse = True
                psar[i] = hp
                lp = low[i]
                af = iaf
        else:
            if high[i] > psar[i]:
                bull = True
                reverse = True
                psar[i] = lp
                hp = high[i]
                af = iaf
    
        if not reverse:
            if bull:
                if high[i] > hp:
                    hp = high[i]
                    af = min(af + iaf, maxaf)
                if low[i - 1] < psar[i]:
                    psar[i] = low[i - 1]
                if low[i - 2] < psar[i]:
                    psar[i] = low[i - 2]
            else:
                if low[i] < lp:
                    lp = low[i]
                    af = min(af + iaf, maxaf)
                if high[i - 1] > psar[i]:
                    psar[i] = high[i - 1]
                if high[i - 2] > psar[i]:
                    psar[i] = high[i - 2]
                    
        if bull:
            psarbull[i] = psar[i]
        else:
            psarbear[i] = psar[i]
 
    return pd.DataFrame({"dates":dates, "high":high, "low":low, "close":close, "psar":psar, "psarbear":psarbear, "psarbull":psarbull})
 
# # ビットコインの相場からSARを算出
# result = psar(df)
# result


# btc = result['close']
btc = df_2019['price']
change = btc.pct_change()

change.head()

trade_return = (change + 1).cumprod()

trade_return[0] = 1

trade_return = trade_return * 10000

# print(trade_return.head(), trade_return[-5:])

price = btc

####複合計算

numpyprice = np.array(price)
# 3 2 25 3
rsi = talib.RSI(price, timeperiod=16) 

momentam = talib.MOM(price, timeperiod=3) / price

macd = talib.MACD(price, fastperiod=12, slowperiod=26, signalperiod=5) 
ema200 = talib.EMA(price, timeperiod=57600)
ema100 = talib.EMA(price, timeperiod=28800)
ema5 = talib.EMA(price, timeperiod=1440)
ema25 = talib.EMA(price, timeperiod=7200)
ema75 = talib.EMA(price, timeperiod=21600)
# ema100 = talib.EMA(price, timeperiod=4000)
signal = [] 

# 日にち単位のSARを計算する
df_2019.index = pd.to_datetime(df_2019['date'])
df_2019_w = df_2019[['price']].resample('D').ohlc()
df_sar = pd.DataFrame(talib.SAR(np.array(df_2019_w.iloc[:,1],dtype='f8'), np.array(df_2019_w.iloc[:,2],dtype='f8')))
df_sar.index = df_2019_w.index
a_sar = pd.DataFrame(df_sar[0].values-df_2019_w.iloc[:,3].values)
a_sar.index = df_2019_w.index
day_sar = a_sar.resample('5T').interpolate()[0]


df_2019_w2 = df_2019[['price']].resample('W').ohlc()
df_sar2 = pd.DataFrame(talib.SAR(np.array(df_2019_w2.iloc[:,1],dtype='f8'), np.array(df_2019_w2.iloc[:,2],dtype='f8')))
df_sar2.index = df_2019_w2.index
b_sar = pd.DataFrame(df_sar2[0].values-df_2019_w2.iloc[:,3].values)
b_sar.index = df_2019_w2.index
week_sar = b_sar.resample('5T').interpolate()[0]


signal = []
term = 28800
#スコアで判定する
for i in range(len(btc)): 
# for i in range(180000,285000): 
    signal_v = 0
    term = 28800
    if i>term:
        ser = btc[i-term:i]
        if len(ser.loc[ser<btc[i]]) == 0:
            signal_v+=-1
#         if len(ser.loc[ser<btc[i]]) != 0 and len(ser.loc[ser>btc[i]]) != 0:
#             signal_v+=-1
    term2 = 57600
    if i>term2:
        ser = btc[i-term2:i]
        if len(ser.loc[ser<btc[i]]) == 0:
            signal_v+=-1
#         if len(ser.loc[ser<btc[i]]) != 0 and len(ser.loc[ser>btc[i]]) != 0:
#             signal_v+=-1
    term3 = 14400
    if i>term2:
        ser = btc[i-term2:i]
        if len(ser.loc[ser<btc[i]]) == 0:
            signal_v+=-1

    term4 = 8640
    if i>term4:
        ser = btc[i-term4:i]
        if len(ser.loc[ser<btc[i]]) == 0:
            signal_v+=-1
        if len(ser.loc[ser<btc[i]]) != 0 and len(ser.loc[ser>btc[i]]) != 0:
            signal_v+=-1

#         if len(ser.loc[ser>btc[i]]) == 0:
#             signal_v+= 1

    if 0.1>momentam[i] >0:
        signal_v+=2
    if day_sar[i] > 0:
        signal_v+=1
    if ema5[i]-ema25[i] > 0:
        signal_v+=1
    if ema100[i]-ema200[i] > 0:
        signal_v+=1
    if ema25[i] - ema75[i] > 0:
        signal_v+=1
#     if week_sar[i] < 0:
#         signal_v+=-1
    if 85>rsi[i] >65:
        signal_v+=1
    if -0.1<momentam[i] < 0:
        signal_v+=-2 
        c+=1
    if  ema5[i]-ema25[i]<0:
        signal_v+=-1
    if  ema25[i]-ema75[i]<0:
        signal_v+=-1
    if  macd[0][i]<0:
        signal_v+=-2
    if  macd[2][i] > 0 or macd[0][i] > 0 :
        signal_v+=1
    if  10<rsi[i] < 40:
        signal_v+=2
        c+=1
        
    signal.append(signal_v)
print(len(signal)-c-n,c,n)


### 累積リターンの計算 ###
#Matplotlibの日本語化
from pylab import rcParams 
import matplotlib as mpl 
font = {"family":"Noto Sans CJK JP"} 
mpl.rc('font', **font) 
rcParams['figure.figsize'] = 15,5 

returns3 = ((change[1:] * signal[:-1]) + 1).cumprod() 
print(returns3[-1:].values[0],len(trade_return),len(returns3))
returns2 = (change + 1).cumprod() 
df2 = pd.DataFrame({'hold':trade_return.values[1:], 'trade':returns3.values}) 
df3 = df2.fillna(method='ffill') 
y1 = np.array(df3['hold']) 
y2 = np.array(df3['trade']) 
x = price.index[0:len(price)-1]
plt.title('トレードリターンの比較') 
plt.plot(x, returns2[0:-1], 'b-', label='ホールドしてた場合のリターン', alpha=0.3, linewidth=1) 
plt.plot(x, returns3, 'orange', label='MACD&モメンタムで取引した場合のリターン', alpha=1, linewidth=1.5) 
plt.ylabel('倍率')
plt.grid(which='both') 
plt.legend()
plt.show()


print('end')
