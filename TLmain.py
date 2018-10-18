'''
Main file of downloading and cleaning data.
Note:
     1: Must check file paths in downloadData_01.py and cleanData_01.py
        before executing.
     2: In order to download files, internet connection is required.      
'''

import downloadData_01 as downloadData
import cleanData_01 as cleanData

'''
 input: year(int), one or two arguement.
 Enter 102 will download and clean all datas of year 102.
 Enter 102, 107 will download and clean all datas from year 102 to year 107.
 '''
def processingData(*year):
    downloadSuccess=downloadData.downloadYear(*year)
    
    for (yearseason, form) in downloadSuccess:
        cleanData.cleanData(yearseason, form)
    print('Execution complete. For details in cleaning data, please check invalidDataLog.txt and outlierLog.txt. ')
    
    return

# exmple: processingData(102)
#      or processingData(102, 107)
processingData(102)
