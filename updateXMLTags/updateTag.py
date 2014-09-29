"""

Date Created: 9/26/2014
Author: Chris Martin
Purpose: Allows for updating a given tag.  Needs revision/clean-up.
        
"""

import os
import xml.etree.ElementTree as ET

def findTag(tag):
    tagToFind = './/' + str(tag)
    try:
        searchTag = tree.find(tagToFind)
        if searchTag is None:
            print 'No', tag
        else:
            print tag + ':', searchTag.text
    except:
        pass
    return searchTag

def createTag(tag):
    if tag == 'origin':
        try:
            print 'Creating <origin>'
            citeinfo = tree.find( './/citeinfo')
            originTag = ET.SubElement(citeinfo,'origin')
            if defaultValue == '':
                valReplacement = raw_input("Enter the new value\n")
                originTag.text = valReplacement
            else:
                originTag.text = defaultValue
        except:
            print 'FAILED TO CREATE TAG'
    if tag == 'publish':
        try:
            print 'Creating <publish>'
            citeinfo = tree.find( './/citeinfo')
            pubinfo = ET.SubElement(citeinfo,'pubinfo')
            publishTag = ET.SubElement(pubinfo, 'publish')
            if defaultValue == '':
                valReplacement = raw_input("Enter the new value\n")
                publishTag.text = valReplacement
            else:
                publishTag.text = defaultValue
        except:
            print 'FAILED TO CREATE TAG'


def writeTag(updateTag):
    try:
        if updateTag.text is None:
            print 'SUCCESS'
            if defaultValue == '':
                valReplacement = raw_input("Enter the new value\n")
                updateTag.text = valReplacement
            else:
                updateTag.text = defaultValue
        else:
            if alterTags in ['y','Y','yes','Yes','YES']:
                if overrideDefault in ['n','N','no','NO','No']:
                    print updateTag.text
                    valCheck = raw_input("Is this value okay? (Y/N)\n")
                    if valCheck in ['n','N','no','NO','No']:
                        valReplacement = raw_input("Enter the new value\n")
                        updateTag.text = valReplacement
                else:
                    updateTag.text = defaultValue
    except:
        print 'Tags unavailable'
        createTag(tag)

while True:
    inputDir = r'D:\drive\Map_Library_Projects\metadata\sources\mn-geospatial-commons'
    tag = raw_input("Tag to find\n")
    defaultValue = raw_input('Enter a default value or press \'enter\' to manually enter per record.\n')
    alterTags = raw_input('Do you want to update tags that already have a value?\n')
    overrideDefault = raw_input("Do you want to override tags with the default value?\n")

    for root, dirs, files in os.walk(inputDir):
        for x in files:
            if x.endswith('.xml'):
                if os.path.isfile(os.path.join(root, x)):
                    filePath = os.path.join(root,x)
                    print filePath
                    tree = ET.parse(filePath)
                    content = tree.getroot()
                    findTag('title')
                    findTag('abstract')

                    # This section was used to set origin <-> publish if one was present
                    '''originTag = findTag('origin')
                    publishTag = findTag('publish')
                    if tag in ['origin', 'publish']:
                        if publishTag is None:
                            if originTag is None:
                                updateTag = findTag(tag)
                                writeTag(updateTag)
                            else:
                                print originTag.text
                                createTag('publish')
                                publishTag = findTag('publish')
                                publishTag.text = originTag.text
                        else:
                            print publishTag.text
                            if originTag is None:
                                createTag('origin')
                                originTag = findTag('origin')
                            originTag.text = publishTag.text
                    else:
                        updateTag = findTag(tag)
                        writeTag(updateTag)'''
                    updateTag = findTag(tag)
                    writeTag(updateTag)
                    try:
                        tree = ET.ElementTree(content)
                        tree.write(filePath)
                        print 'Wrote new XML'
                    except:
                        print "FAILED TO WRITE NEW XML"
    runAgain = raw_input("Run again?\n")
    if runAgain not in ['', 'y', 'yes', 'Y', 'YES']:
        exit()
