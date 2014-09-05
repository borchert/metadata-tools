import os
import shutil

def getDrivePath():
    while True:
        drivePath = raw_input("Please enter the path to your Drive folder (i.e. D:\drive or C:\Users\username\Google "
                              "Drive):  ")
        if not os.path.exists(drivePath):
            print 'That path does not work.  Please try again.'
        else:
            break
    return drivePath

if os.path.exists(r'D:\drive\\'):
    drivePath = r'D:\drive\Map Library Projects'
elif os.path.exists(os.path.join(r'C:\Users\\',userName,'Google Drive')):
    drivePath = os.path.join(r'C:\Users\\',userName,'Google Drive\Map Library Projects')
else:
    drivePath = getDrivePath()

startDir = r'C:\Users\mart3565\Downloads\pub'
outPathDir = os.path.join(drivePath, 'MN Geospatial Commons\\data\\renamed_metadata_xmls')

for root, dirs, files in os.walk(startDir):
    for f in files:
        if f.startswith('meta'):
            filePath = os.path.join(root, f)

            prefix = filePath[38:len(filePath)-22]
            for i in prefix:
                if i == '\\':
                    prefix = prefix.replace(i, '_')

            outFile = os.path.join(outPathDir, prefix + '_metadata.xml')
            if os.path.isfile(outFile):
                print 'REMOVED', outFile
                os.remove(outFile)

            print 'WRITING -', outFile

            shutil.copy(os.path.join(root,f), outFile)

