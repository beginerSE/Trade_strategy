import talib

def cal_backtest(price,mterm1=12,mterm2=26,mterm3=5,momterm=6):
    numpyprice=np.array(price)
    change=price.pct_change()
    hold_return=(change+1).cumprod()
    hold_return[0]=1
    hold_return=trade_return*10000
    momentam=talib.MOM(price,timeperiod=momterm)
    macd=talib.MACD(price,fastperiod=mterm1, slowperiod=mterm2,    signalperiod=mterm3)
    signal=[]
    for i in range(len(price)):
        if momentam[i]>0 and macd[2][i] >0:
            signal.append(1)
        elif momentam[i]<0 and macd[2][i]<0 :
            signal.append(-1)
        else:
            signal.append(0)
    ##累積リターンの計算##累積リターンの計算
    trade_returns=((change[1:]*signal[:-1])+1).cumprod()
    df=pd.DataFrame({'hold':hold_return,'trade':trade_returns})
    df3=df2.fillna(method='ffill')
    y1=np.array(df3['hold'])
    y2=np.array(df3['trade'])
    x=price.index[0:len(price)-1]
    return trade_returns[-1]

 
#バックテスト関数を実行する
cal_backtest(price,mterm1=12,mterm2=26,mterm3=5,momterm=6)
