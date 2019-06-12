import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style


x, y_WH, y_XI, y_BT=[], [], [], []


readLoc='C:/Users/Yotti/Desktop/TL_hw/output/'

for year in range(102, 108):
    for season in range(1, 5):
        readPath = readLoc+'cleaned_'+str(year)+'S'+str(season)+'_A_lvr_land_A.CSV'
        df = pd.read_csv(readPath, index_col=False, encoding = 'utf8', skiprows=range(1, 2))
        
        #信義
        df_XI=df.loc[(df['鄉鎮市區'] == 3) & (df['outlier']==0)]
        df_XI=df_XI[['建物移轉總面積平方公尺', '總價元']].sum()
        avg_price_XI=df_XI['總價元']/df_XI['建物移轉總面積平方公尺']
        y_XI.append(avg_price_XI)
        x.append(str(year)+'S'+str(season))
        
        #萬華
        df_WH=df.loc[(df['鄉鎮市區'] == 12) & (df['outlier']==0)]
        df_WH=df_WH[['建物移轉總面積平方公尺', '總價元']].sum()
        avg_price_WH=df_WH['總價元']/df_WH['建物移轉總面積平方公尺']
        y_WH.append(avg_price_WH)
        
        #內湖
        df_BT=df.loc[(df['鄉鎮市區'] == 4) & (df['outlier']==0)]
        df_BT=df_BT[['建物移轉總面積平方公尺', '總價元']].sum()
        avg_price_BT=df_BT['總價元']/df_BT['建物移轉總面積平方公尺']
        y_BT.append(avg_price_BT)




style.use('ggplot')

plt.plot(x, y_XI, 's-', label='Xinyi')
plt.plot(x, y_WH, 'o-', label='Wanhua')
plt.plot(x, y_BT, 'gx-', label='Neihu')
plt.xlabel('seasons')
plt.ylabel('price per m^2')
plt.legend()
plt.show()
