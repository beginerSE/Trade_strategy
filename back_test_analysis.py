
##累積リターンの計算

from pylab import rcParams
import matplotlib as mpl


# プロットの初期設定を変更する(日本語化設定している人はスルーしてください)
font = {"family":"Noto Sans CJK JP"}
mpl.rc('font', **font)
rcParams['figure.figsize'] = 10,5


# ホールドのリターンを検証する
returns2=(price.pct_change()+1).cumprod()
returns3=cal_backtest(price,17,15,3,6)
df=pd.DataFrame({'hold':returns2,'trade':returns3})
df3=df.fillna(method='ffill')
x=returns2[1:].index
print(len(returns2),len(returns3))
print(returns2.head())
plt.title('トレードリターンの比較')
plt.plot(x,returns2[1:],'b-',label='ホールドしてた場合のリターン',alpha=0.3,linewidth=1)
plt.plot(x,returns3,'orange',label='トレード戦略に沿って取引した場合のリターン',alpha=1,linewidth=1.5)
plt.ylabel('倍率')
plt.grid(which='both')
plt.legend()
# 出力した画像を保存する
plt.savefig('sample.png')


#returns3は戦略によるトレード利益推移のデータ


#最大ドローダウンの計算
dro=[]
for i in range(len(returns3)):
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
print('リターン',returns3[-1])


# 年次リターンを計算する
for i in ['2013','2014','2015','2016','2017','2018','2019']:
    returns_year=returns3[i+'-01-01':i+'-12-31']
    print(i+'年の年次リターン :',str((returns_year[-1]-returns_year[0])/returns_year[0]*100)+'%')
