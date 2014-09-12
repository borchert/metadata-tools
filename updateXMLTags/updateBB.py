"""

Date Created: 9/12/2014
Author: Chris Martin
Purpose: Checks all <northbc>, <southbc> xml tags for accuracy (removes incorrect negative values, incorrect values.
        
"""


import os
import xml.etree.ElementTree as ET
import csv

inputDir = 'D:\drive\Map Library Projects\MGS\Records'
failedNBC =[]
failedSBC =[]
northBoundingCoordinate = ''
southBoundingCoordinate = ''
failedBBFiles = {}
fixableBBFiles = {}
failedBBOut = r'c:/users/mart3565/desktop/failedBB.csv'
fixableBBOut = r'c:/users/mart3565/desktop/fixableBB.csv'
drivePath = r'd:drive/Map Library Projects/MGS'

# FIX 'fixable' BBs

with open(fixableBBOut, "r") as f:
    reader = csv.reader(f)
    result = {}
    rowcount = 0
    for row in reader:
        if rowcount == 0:
            rowcount += 1
            continue

        else:
            key = row[0]
            fixableBBFiles[key] = row[1:]

for key, value in fixableBBFiles.items():
    print key

    tree = ET.parse(key)
    content = tree.getroot()
    try:
        try:
            findTag = tree.find('.//northbc')
            print findTag
            northBoundingCoordinate = value[0]
            print northBoundingCoordinate
            findTag.text = northBoundingCoordinate
        except:
            print 'help'
        findTag = tree.find('.//southbc')
        southBoundingCoordinate = value[1]
        print southBoundingCoordinate
        findTag.text = southBoundingCoordinate

    except:
        print 'really help'
    raw_input()

'''onlink.text = linkDict[record]
        except:
            citeinfo = tree.find( './/citeinfo' )
            onlink = ET.SubElement(citeinfo,'onlink')
            onlink.text = linkDict[record]

        ET.dump(onlink)
        tree = ET.ElementTree(content)
        tree.write(filePath)
    except:
        failed.append(filePath)'''

'''count = 0
for key in fixableBBFiles:
    if key[48:49] == '\\':
        record = key[42:48]
    elif key[48:49] == 'f':
        record = key[42:47]
    elif key[48:49] == 'i':
        record = key[42:46]
    elif key[48:49] == 'n':
        record = key[42:45]'''



'''# FIX 'failed' BBs

with open(failedBBFiles, "r") as f:
    reader = csv.reader(f)
    result = {}
    rowcount = 0
    for row in reader:
        if rowcount == 0:
            rowcount += 1
            continue

        else:
            key = row[0]
            failedBBFiles[key] = row[1:]


count = 0
for key in failedBBFiles:
    if key[48:49] == '\\':
        record = key[42:48]
    elif key[48:49] == 'f':
        record = key[42:47]
    elif key[48:49] == 'i':
        record = key[42:46]
    elif key[48:49] == 'n':
        record = key[42:45]


    searchPath = os.path.join(drivePath, 'Records', record)
    shapefile = key[len(searchPath)+13:len(key)-4]

    for root, dirs, files in os.walk(searchPath):
        for f in files:
            if f == shapefile:
                if os.path.isfile(os.path.join(root, f)):
                    print os.path.join(root, f), '\n'
            elif f == shapefile +'.shp':
                if os.path.isfile(os.path.join(root, f)):
                    print os.path.join(root, f), '\n'''''

#Used to generate CSV output
'''for root, dirs, files in os.walk(inputDir):
    if root[len(root)-10:] == 'final_XMLs':
        for f in files:
            if f.endswith('.xml'):
                if f.endswith('template.xml'):
                    continue
                filePath = os.path.join(root,f)
                tree = ET.parse(filePath)
                content = tree.getroot()

                try:
                    northbc = tree.find('.//northbc')
                    northBoundingCoordinate = northbc.text

                except:
                    failedNBC.append(filePath)
                try:
                    southbc = tree.find('.//southbc')
                    southBoundingCoordinate = southbc.text

                except:
                    failedSBC.append(filePath)

                if northBoundingCoordinate[0:1] == '-' or southBoundingCoordinate[0:1] == '-':
                    if northBoundingCoordinate[1:2] == '4':
                        value = northBoundingCoordinate[1:], southBoundingCoordinate[1:]
                        fixableBBFiles[filePath] = value
                    else:
                        value = northBoundingCoordinate, southBoundingCoordinate
                        failedBBFiles[filePath] = value
                elif northBoundingCoordinate[0:1] == '0' or southBoundingCoordinate[0:1] == '0':
                    value = northBoundingCoordinate, southBoundingCoordinate
                    failedBBFiles[filePath] = value

f = open(fixableBBOut,'a')
writer = csv.writer(f)
writer.writerow( ('Record', 'North', 'South'))
for key, value in fixableBBFiles.items():
    writer.writerow((key, value[0], value[1]))
f.close

f = open(failedBBOut, 'a')
writer = csv.writer(f)
writer.writerow( ('Record', 'North', 'South'))
for key, value in failedBBFiles.items():
    writer.writerow((key, value[0], value[1]))
f.close'''
