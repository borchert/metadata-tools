"""

Date Created: 9/26/2014
Author: Chris Martin
Purpose: Cleans up <title> xml tags by printing current value and asking for user input of new value, if any.
        
"""


import os
import xml.etree.ElementTree as ET

inputDir = r'D:\drive\Map_Library_Projects\metadata\sources\dakota-county'

for root, dirs, files in os.walk(inputDir):
    for f in files:
        if f.endswith('.xml'):
            filePath = os.path.join(root,f)
            tree = ET.parse(filePath)
            content = tree.getroot()
            try:
                title = tree.find('.//title')
                titleText = title.text
                print "Title = ",titleText
            except:
                print 'No title available\n'
            try:
                abstract = tree.find('.//abstract')
                abstractText = abstract.text
                print "Abstract = ", abstractText
            except:
                print 'No abstract available\n'
            try:
                changeVal = raw_input("Enter the new value for the title or 's' to skip\n")
                if changeVal not in ['s', 'S']:
                    title.text = changeVal
                    print 'Changing to: ', title.text
                    raw_input()
                    tree = ET.ElementTree(content)
                    tree.write(filePath)

            except:
                print 'Failed to update title.'