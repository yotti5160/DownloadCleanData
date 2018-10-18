'''
Module for downloading data, note that dataLoc in line 17 may need modification.
This module need internet connection to be properly executed.
'''

import os
import urllib


'''
 One input or two inputs(int).
 If one, download the data of that year. If two, say y1 and y2, download data form year y1 to year y2. 
 Return years and seasons download successfully(list of tuples), each tuple of the form (yearSeason , form), e.g. ('102S1', 'A').
 '''
def downloadYear(*year):
    
    # dataLoc: folder to save download files
    dataLoc = 'C:/Users/Yotti/Desktop/TL_hw/download'
    
    url_part = [
            "http://plvr.land.moi.gov.tw/DownloadSeason?season=",
            "&type=zip&fileName=",
            "lvr_land",
            ".csv"
            ]
    forms = ['A', 'B', 'C']
    output = []
        
    # One input, download data of four seasons of that year.
    def download(y):
        for i in range(1,5):
            file = str(y) + "S" + str(i)
            for c in forms:
                fileName = file + '_A_' + url_part[2] + '_' + c + url_part[3]
                url = url_part[0] + file + url_part[1] + 'A_' + url_part[2] + '_' + c + url_part[3]
                
                try:
                    resp = urllib.request.urlopen(url)
                    ct = resp.info()['Content-Type']
                    if ct[:3]=='app':
                        localPath = os.path.join(dataLoc, fileName)
                        urllib.request.urlretrieve(url,localPath)
                        print(fileName + ' downloaded successfully.')
                        output.append((file, c))
                    elif ct[:3]=='tex':
                        print(fileName + ' doesn\'t exist.')
                except Exception as e:
                    print(fileName + ' error: ', e)

    if len(year)==1:
        download(year[0])
    elif len(year)==2:
        for y in range(year[0], year[1]+1):
            download(y)
    return output

