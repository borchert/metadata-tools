"""

Date Created: 9/26/2014
Author: Chris Martin
Purpose: Cleans up <title> xml tags by printing current value and asking for user input of new value, if any.
        
"""


import os
import xml.etree.ElementTree as ET

inputDir = r'D:\drive\Map_Library_Projects\metadata\sources\ramsey-county'

'''dates = r'C:\Users\mart3565\Desktop\dakota_dates.csv'
datesList = []
f = open(dates, 'r')
content = f.readlines()
for x in content:
    datesList.append(x[:-1])'''

for root, dirs, files in os.walk(inputDir):
    #for x in datesList:
    for x in files:
        if x.endswith('.xml'):
            if os.path.isfile(os.path.join(root, x)):
                filePath = os.path.join(root,x)
                print filePath
                tree = ET.parse(filePath)
                content = tree.getroot()
                try:
                    pubDateTag = tree.find('.//pubdate')
                    if pubDateTag.text is None:
                        pubDateTag.text = str(2014)
                    else:
                        print pubDateTag.text
                    print 'Set it way one'
                except:
                    print 'Creating tags'
                    try:
                        citeinfo = tree.find( './/citeinfo' )
                        pubDateTag = ET.SubElement(citeinfo,'pubdate')
                        pubDateTag.text = str(2014)
                        print 'set it way two'
                    except:
                        break
                try:
                    tree = ET.ElementTree(content)
                    tree.write(filePath)
                except:
                    print "FAILED"