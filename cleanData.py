'''
Module for cleaning data.
Note that readLoc, writeLoc, invalidDataLogLoc, 
outlierLogLoc and dbLoc in line 22 to line 24 may need modification.
And, readLoc in line 16 must be the same as dataLoc in line 18 of downloadData.py
'''
import pandas as pd
import sqlite3
import collections
import os

# Two inputs, yearSeason(string) and form(string)
def cleanData(yearSeason, form):  
    
    # readLoc: folder for download data  
    readLoc='C:/Users/Yotti/Desktop/TL_hw/download'
    # writeLoc: folder for output data(cleaned data)
    writeLoc='C:/Users/Yotti/Desktop/TL_hw/output'
    # invalidDataLogLoc: location for log of invalid data 
    invalidDataLogLoc='C:/Users/Yotti/Desktop/TL_hw/output/invalidDataLog.txt'
    # outlierLogLoc: location for log of outliers
    outlierLogLoc='C:/Users/Yotti/Desktop/TL_hw/output/outlierLog.txt'
    # dbLoc: location of SQLite database
    dbLoc='C:/Users/Yotti/Desktop/TL_hw/output/test.db'
    
    # dictionary for change data
    CATEGORY_MAP = {'主要建材': {'': 0,
    '加強磚造': 1,
     '土木造': 2,
    '土磚石混合造': 3,
    '土造': 4,'壁式預鑄鋼筋混凝土造': 5,
                 '木造': 6,
    '石造': 7,
     '磚造': 8,
    '見使用執照': 9,
     '見其他登記事項': 10,
     '鋼筋混凝土加強磚造': 11,
     '鋼筋混凝土造': 12, '鋼骨混凝土造': 13,
    '鋼骨鋼筋混凝土造': 14,'鐵造': 15,'預力混凝土造': 16},
        
    '主要用途': {'': 0,'住商用': 1,
    '住家用': 2,
    '住工用': 3,'停車空間': 4,'商業用': 5,
    '工商用': 6,
    '工業用': 7,'見使用執照': 8,
                 '見其他登記事項': 9,
    '農舍': 10},
        
    '建物型態': {'': 0,
    '住宅大樓(11層含以上有電梯)': 1,'倉庫': 2,
    '公寓(5樓含以下無電梯)': 3,'其他': 4,'套房(1房1廳1衛)': 5,
    '工廠': 6,
        '店面(店鋪)': 7,'廠辦': 8,'華廈(10層含以下有電梯)': 9,
    '辦公商業大樓': 10,
     '農舍': 11,
    '透天厝': 12},
    '都市土地使用分區': {'': 0, '住': 1, '其他': 2, '商': 3, '工': 4, '農': 5},
      
    '鄉鎮市區': {'': 0,
    '中山區': 1,
    '中正區': 2, '信義區': 3,'內湖區': 4,
    '北投區': 5,
    '南港區': 6,'士林區': 7,'大同區': 8,
                 '大安區': 9,
                 '文山區': 10,
                 '松山區': 11,
                 '萬華區': 12},
      
    '車位類別': {'': 0,
                 '坡道平面': 1,
                 '升降平面': 2,
                 '坡道機械': 3,
                 '升降機械': 4,
                 '塔式車位': 5,
                 '一樓平面': 6,
                 '其他': 7,
        },
    }
    
    # read file, there are two types of encoding 'utf8' and 'ansi'
    readPath = os.path.join(readLoc, yearSeason+'_A_lvr_land_'+form+'.CSV')
    try:
        df = pd.read_csv(readPath, index_col=False, encoding = 'utf8', skiprows=range(1, 2))
        print(yearSeason+'_A_lvr_land_'+form+'.CSV' + ' decode with utf8 success.')
    except Exception as e:
        print('error: ', e)
        return
        
    # badDatas: collect bad datas
    # rowsToDrop: collect index for bad datas
    badDatas, rowsToDrop=[], []
    
    # Find columns need to change (string to int)
    needToChange=[]
    for colName in df.columns:
        if colName in CATEGORY_MAP:
            needToChange.append(colName)
    
    for index,row in df.iterrows():
        for colName in needToChange:
            if not pd.isnull(row[colName]):
                try:
                    df.at[index, colName]=CATEGORY_MAP[colName][row[colName]]
                except:
                    badDatas.append([index, colName, row[colName], 'catagory error.'])
                    if not rowsToDrop or rowsToDrop[-1]!=index:
                        rowsToDrop.append(index)
            else:
                df.at[index, colName]=CATEGORY_MAP[colName]['']
    
    # write invalidDataLog log
    f=open(invalidDataLogLoc, 'a')
    f.write('In cleaning '+yearSeason+'_A_lvr_land_'+form+'.CSV: \n')
    if badDatas:
        f.write('The following are invalid datas:\n')
        for baddata in  badDatas:
            f.write(''.join(['Data index:', str(baddata[0]), '(row ', str(baddata[0]+3), ' in CSV file), column ', str(baddata[1]), ':', str(baddata[2]), ' ,which is not in CATEGORY_MAP.\n']))
        f.write('Total number of bad datas: '+str(len(badDatas))+'\n')
    else:
        f.write('Found no error in data processing.\n')
    f.write(''.join(['There are ',str(len(df)-len(badDatas)),' rows of data in output file ','cleaned_',yearSeason,'_A_lvr_land_',form,'.CSV','.\n\n']))
    f.close()

    # drop invalid rows
    df.drop(df.index[rowsToDrop], inplace=True)
    
    # find outliers on '單價(元/平方公尺)' (by IQR)
    dic_Q1=df.groupby(['鄉鎮市區', '建物型態'])['單價元/平方公尺'].quantile(.25).to_dict()
    dic_Q3=df.groupby(['鄉鎮市區', '建物型態'])['單價元/平方公尺'].quantile(.75).to_dict()    
       
    groupIQRrange=collections.defaultdict(list) # contain good data range of each district and building type.
    for key in dic_Q1:
        tmpQ1, tmpQ3=dic_Q1[key], dic_Q3[key]
        tmpIQR=tmpQ3-tmpQ1
        groupIQRrange[key]=[[tmpQ1-1.5*tmpIQR, tmpQ3+1.5*tmpIQR], [tmpQ1-3*tmpIQR, tmpQ3+3*tmpIQR]]
    
    # add column 'outlier', value=0 for normal data, value=1 for to outlier, value=2 for far outlier
    df = df.assign(outlier = [0]*len(df))
    
    outlierBook, outlierCount, farOutlierCount=[], 0, 0
    for index,row in df.iterrows():
        if not pd.isnull(row['單價元/平方公尺']):
            if row['單價元/平方公尺']>groupIQRrange[(row['鄉鎮市區'], row['建物型態'])][1][1] or row['單價元/平方公尺']<groupIQRrange[(row['鄉鎮市區'], row['建物型態'])][1][0]:
                outlierBook.append((index, 2))
                farOutlierCount+=1
                df.at[index, 'outlier']=2
            elif row['單價元/平方公尺']>groupIQRrange[(row['鄉鎮市區'], row['建物型態'])][0][1] or row['單價元/平方公尺']<groupIQRrange[(row['鄉鎮市區'], row['建物型態'])][0][0]:
                outlierBook.append((index, 1))
                outlierCount+=1
                df.at[index, 'outlier']=1
    
    # write outlier log
    f=open(outlierLogLoc, 'a')
    f.write('In '+yearSeason+'_A_lvr_land_'+form+'.CSV: \n')
    if outlierBook:
        f.write('The following are outliers and far outliers:\n')
        for outlier in  outlierBook:
            if outlier[1]==1:
                f.write(''.join(['Data index: ', str(outlier[0]), '(row ', str(outlier[0]+3), ' in CSV file) is an outlier. \n']))
            else:
                f.write(''.join(['Data index: ', str(outlier[0]), '(row ', str(outlier[0]+3), ' in CSV file) is a far outlier. \n']))
    else:
        f.write('Found no outlier in data processing.\n')
    f.write(''.join(['There are ',str(outlierCount),' outliers and ',str(farOutlierCount), ' far outliers in ',yearSeason,'_A_lvr_land_',form,'.CSV','.\n\n']))
    f.close()
    
    # output cleaned data to csv  
    writePath = os.path.join(writeLoc, 'cleaned_'+yearSeason+'_A_lvr_land_'+form)       
    df.to_csv(writePath+'.CSV', index=False, encoding='utf-8-sig')  
    
    # output cleaned data to msgpack  
    df.to_msgpack(writePath+'.msgpack', encoding='utf-8-sig')
    
    # output cleaned data to SQLite
    conn=sqlite3.connect(dbLoc)
    df.to_sql('cleaned_'+yearSeason+'_A_lvr_land_'+form, conn, if_exists='replace', index=True, index_label=None)
    conn.close()
    
    print('Cleaning '+yearSeason+'_A_lvr_land_'+form+' completed.')
    
    return
