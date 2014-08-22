import os
import subprocess

def getDrivePath():
    while True:
        drivePath = raw_input("Please enter the path to your Drive folder (i.e. D:\drive or C:\Users\username\Google "
                              "Drive):  ")
        if not os.path.exists(drivePath):
            print 'That path does not work.  Please try again.'
        else:
            break
    return drivePath

userName = os.environ.get('USERNAME')

if os.path.exists(r'D:\drive\\'):
    drivePath = r'D:\drive\Map Library Projects\MGS'
elif os.path.exists(os.path.join(r'C:\Users\\',userName,'Google Drive')):
    drivePath = os.path.join(r'C:\Users\\',userName,'Google Drive\Map Library Projects\MGS')
else:
    drivePath = getDrivePath()

startDir = drivePath + '\\Records'
failedLineage = drivePath + '\\failedLineage.txt'
failedAbstract = drivePath + '\\failedAbstract.txt'
failedHorizontal = drivePath + '\\failedHorizontal.txt'
failedMapUnits = drivePath + '\\failedMapUnits.txt'
failedPurpose = drivePath + '\\failedPurpose.txt'
failedPubDate = drivePath + '\\failedPubDate.txt'
failedAll = drivePath + '\\failedAll.txt'

fileList = [failedAbstract,failedLineage,failedHorizontal,failedMapUnits,failedPurpose,failedPubDate,failedAll]

tagDict = {failedLineage:'lineageT\n',
           failedAbstract:'abstractT\n',
           failedHorizontal:'horizontalPositionalAccuracyT\n',
           failedMapUnits:'mapUnitsT\n',
           failedPurpose:'purposeT\n',
           failedPubDate:'publicationDateT'
}

for x in fileList:
    if os.path.isfile(x):
        os.remove(x)
        print 'Removed', x
        
for root, dirs ,files in os.walk(startDir):
    for file in files:
        if file.endswith('failedtags.txt'):
            path = os.path.join(root,file)
            with open(path) as f:
                content = f.readlines()
                for x in content:
                    output = [root, '\\', file, '\n']

                    for key, val in tagDict.items():
                        if x == val:
                            f = open(key, 'a')
                            f.write(''.join(output))
                            f.close

abstract_num_lines = sum(1 for line in open(failedAbstract))
horiz_num_lines = sum(1 for line in open(failedHorizontal))
lineage_num_lines = sum(1 for line in open(failedLineage))
mapUnits_num_lines = sum(1 for line in open(failedMapUnits))
#pubDate_num_lines = sum(1 for line in open(failedPubDate))
purpose_num_lines = sum(1 for line in open(failedPurpose))

pubDate_num_lines = '0'

countDict= {failedAbstract:abstract_num_lines,
             failedHorizontal:horiz_num_lines,
             failedLineage:lineage_num_lines,
             failedMapUnits:mapUnits_num_lines,
             failedPubDate:pubDate_num_lines,
             failedPurpose:purpose_num_lines
}

for key,val in countDict.items():
    output = '\nNumber of files: ', str(countDict[key])
    f = open(key,'a')
    f.write(''.join(output))
    f.close

failedAbstractList = []
with open(failedAbstract) as f:
    content = f.readlines()
    for x in content:
        failedAbstractList.append(x[:-1])

failedLineageList = []
with open(failedLineage) as f:
    content = f.readlines()
    for x in content:
        failedLineageList.append(x[:-1])

failedPubDateList = []
with open(failedPubDate) as f:
    content = f.readlines()
    for x in content:
        failedPubDateList.append(x[:-1])

failedPurposeList = []
with open(failedPurpose) as f:
    content = f.readlines()
    for x in content:
        failedPurposeList.append(x[:-1])

failedHorizList = []
with open(failedHorizontal) as f:
    content = f.readlines()
    for x in content:
        failedHorizList.append(x[:-1])

failedMapList = []
with open(failedMapUnits) as f:
    content = f.readlines()
    for x in content:
        failedMapList.append(x[:-1])

for x in failedAbstractList:
    if x in failedLineageList:
        if x in failedPurposeList:
            if x in failedHorizList:
                if x in failedMapList:
                    output = x, '\n'
                    f = open(failedAll,'a')
                    f.write(''.join(output))
                    f.close

failedAllList = []
with open(failedAll) as f:
    content = f.readlines()
    for x in content:
        failedAllList.append(x[:-1])

count = 0
for x in failedAllList:

    path = x[:68] +'temporary/'
    if os.path.exists(path):
        pass
    else:
        path = x[:67] +'temporary/'
        if os.path.exists(path):
            pass
        else:
            path = x[:66] +'temporary/'
            if os.path.exists(path):
                pass
            else:
                path = x[:65] +'temporary/'

    f = x[len(path):-15]+'.txt'

    builtPath = path + f

    if count < 5:
        subprocess.Popen([r'C:\Program Files (x86)\Notepad++\notepad++.exe', builtPath])
        count+=1
    else:
        raw_input()
        count = 0


