此程式的功能為到 http://plvr.land.moi.gov.tw/DownloadOpenData 下載台北市的不動產交易資料，整理資料後再輸出檔案。  


共有4個.py檔:  

* main.py  
* downloadData.py  
* cleanData.py
* CATEGORY_MAP.py

main.py會使用downloadData.py和cleanData.py模組，在執行main.py前請確認有網路連線，也設定好downloatData.py和cleanData.py中的file path, 以確保讀寫檔能順利進行。CATEGORY_MAP.py為整理資料時的規則，會將下載檔案中的一些column的資料轉換為整數。  

以下對檔案的運作簡單的說明:  

<img src="https://github.com/yotti5160/DownloadCleanDataExercise/blob/master/screenshot01.PNG" width="500">









下載的檔案命名方式如下:  

102年第一季的
* 不動產買賣為102S1_A_lvr_land_A.csv   
* 預售屋買賣為102S1_A_lvr_land_B.csv             
* 不動產租賃為102S1_A_lvr_land_C.csv   
             
在整理資料時，Bad data是在將字串轉換為int時，不在category_map.py中的資料，Bad data不會被輸出，執行完會有一個invalidDataLog.txt，其中記錄了整理資料時的Bad data，以及輸出檔的資料筆數。   

而Abnormal data(outlier)是在"鄉鎮市區"和"建物型態"的分群下，"單價(元/平方公尺)"數值太極端的資料，極端數值的範圍是由Interquartile Range (IQR)所定義，數值低於Q1-1.5IQR或高於Q3+1.5IQR者視為outlier，其中數值低於Q1-3IQR或高於Q3+3IQR者視為far outlier。   

在輸出的檔案多加了一個"outlier" column，一般資料的值為0，outlier的值為1，far outlier的值為2。執行完會有一個outlierLog.txt，記錄了處理資料中的outlier和far outlier。 
