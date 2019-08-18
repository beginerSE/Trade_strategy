rsi = talib.RSI(price, timeperiod=2)
signal=[]

for i in range(2028):
    if rsi[i]>70:
        signal.append(1)
    elif rsi[i]<30:
        signal.append(-1)
    else:
        signal.append(0)

        
##累積リターンの計算

from pylab import rcParams
import matplotlib as mpl
font = {"family":"Noto Sans CJK JP"}
mpl.rc('font', **font)


rcParams['figure.figsize'] = 10,5
returns3=((change[1:2028]*signal[0:2027])+1).cumprod()
returns2=(change+1).cumprod()
df2=pd.DataFrame({'hold':returns2,'trade':returns})
df3=df2.fillna(method='ffill')
y1=np.array(df3['hold'])
y2=np.array(df3['trade'])
#x=df.index
x=df.index[0:2027]

plt.title('トレードリターンの比較')

plt.plot(x,returns2[0:2027],'b-',label='ホールドしてた場合のリターン',alpha=0.3,linewidth=1)
plt.plot(x,returns3,'orange',label='RSIで取引した場合のリターン',alpha=1,linewidth=1.5)
plt.ylabel('倍率')
plt.grid(which='both')
plt.legend()
# 出力した画像を保存する
plt.savefig('sample.png')


#returns3は戦略によるトレード利益推移のデータ


#最大ドローダウンの計算
dro=[]
for i in range(2026):
    max=returns3[:i].max()
    drop=max-returns3[i]
    dro.append(drop)
dhi=dro[2:]
sdi=np.array(dhi)
s=sdi.max()
print('最大ドローダウン',(1-(max-s)/max)*100)


#勝率の計算方法・勝ちトレード数÷全トレード数
#ペイオフレシオの計算方法：勝ちトレードの平均利益額÷負けトレードの平均損失額

returndiff=returns3.diff()
paydata=returndiff.fillna(method='ffill')
win=[]
lose=[]

for i in paydata:
    if i>0:
        win.append(i)
    if i<0:
        lose.append(i)
print('勝率',len(win)/(len(win)+len(lose))*100)


loseprice=sum(lose)/len(lose)
winprice=sum(win)/len(win)
print('ペイオフレシオ',winprice/loseprice*-1)


#プロフィットファクターの計算方法：純利益÷純損失

print('プロフィットファクター',sum(win)/sum(lose)*-1)
print('リターン',returns3[2026])
