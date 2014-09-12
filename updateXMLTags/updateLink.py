"""

Date Created: 9/12/2014
Author: Chris Martin
Purpose: Updates all <onlink> xml tags to value found in dictionary.  Dictionary is read in as a CSV with (record,link)
        column format.
        
"""


import os
import xml.etree.ElementTree as ET
import csv

inputDir = 'D:\drive\Map Library Projects\MGS\Records'
links = 'c:/users/mart3565/desktop/recordslinks.csv'

with open(links, mode='r') as infile:
    reader = csv.reader(infile)
    linkDict = {rows[0]:rows[1] for rows in reader}

failed = []

for root, dirs, files in os.walk(inputDir):
    if root[len(root)-10:] == 'final_XMLs':
        for f in files:
            if f.endswith('.xml'):
                filePath = os.path.join(root,f)
                print 'Working on - ', filePath
                if filePath[42:48] in linkDict:
                    record = filePath[42:48]
                elif filePath[42:47] in linkDict:
                    record = filePath[42:47]
                elif filePath[42:46] in linkDict:
                    record = filePath[42:46]
                elif filePath[42:45] in linkDict:
                    record = filePath[42:45]
                tree = ET.parse(filePath)
                content = tree.getroot()
                try:
                    try:
                        onlink = tree.find('.//onlink')
                        link = onlink.text
                        onlink.text = linkDict[record]
                    except:
                        citeinfo = tree.find( './/citeinfo' )
                        onlink = ET.SubElement(citeinfo,'onlink')
                        onlink.text = linkDict[record]

                    ET.dump(onlink)
                    tree = ET.ElementTree(content)
                    tree.write(filePath)
                except:
                    failed.append(filePath)

failedLinks = r'c:/users/mart3565/desktop/failedLinks.txt'
f = open(failedLinks, 'w')
for x in failed:
    f.write(x)
    f.write('\n')
f.close