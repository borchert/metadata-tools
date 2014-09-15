"""

Date Created: 9/12/2014
Author: Chris Martin
Purpose: Corrects failed or incomplete bounding box tags.

    def negative_BB(): Checks all <northbc>, <southbc> xml tags for accuracy (removes incorrect negative values,
    incorrect values.

    def failed_BB():  Runs processShapefile on the corresponding shapefile for each failed BB's XML.  Updates with
    correct values
        
"""


import os
import xml.etree.ElementTree as ET
import csv
import arcpy

inputDir = 'D:\drive\Map Library Projects\MGS\Records'
failedNBC =[]
failedSBC =[]
failed = []
northBoundingCoordinate = ''
southBoundingCoordinate = ''
failedBBFiles = {}
fixableBBFiles = {}
failedBBOut = r'c:/users/mart3565/desktop/failedBB.csv'
fixableBBOut = r'c:/users/mart3565/desktop/fixableBB.csv'
weirdBBOut = r'c:/users/mart3565/desktop/weirdBBOut.csv'
drivePath = r'd:drive/Map Library Projects/MGS'

def negative_BB():

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

     # USED TO FIX NEGATIVE BB records
    for key, value in fixableBBFiles.items():
        print key

        tree = ET.parse(key)
        content = tree.getroot()
        try:
            northBCTag = tree.find('.//northbc')
            northBoundingCoordinate = value[0]
            #print northBoundingCoordinate
            if northBCTag is None:
                print 'Creating tags'
                spdom = tree.find( './/spdom' )
                bounding = ET.SubElement(spdom,'bounding')
                northBC = ET.SubElement(bounding,'northbc')
                southBC = ET.SubElement(bounding,'southbc')
                northBC.text = northBoundingCoordinate
                ET.dump(northBC)
            else:
                northBCTag.text = northBoundingCoordinate
                ET.dump(northBCTag)
        except:
            print 'Couldn\'t find north bb.'
            raw_input()

        try:
            southBCTag = tree.find('.//southbc')
            southBoundingCoordinate = value[1]
            print southBoundingCoordinate
            if southBCTag is None:
                southBC.text = southBoundingCoordinate
                ET.dump(southBC)
            else:
                southBCTag.text = southBoundingCoordinate
                ET.dump(southBCTag)
        except:
            print 'Couldn\'t find south bb.'
            raw_input()

        try:
            tree = ET.ElementTree(content)
            print 'OVERWRITING -', key
            #raw_input('Press enter if this is alright.')
            tree.write(key)
        except:
            failed.append(key)

    print failed

def failed_BB ():
    count = 0
    # FIX 'failed' BBs
    with open(failedBBOut, "r") as f:
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
                        shpPath = os.path.join(root, f)

                elif f == shapefile +'.shp':
                    if os.path.isfile(os.path.join(root, f)):
                        shpPath = os.path.join(root, f)

        extent = processShapefile(shpPath)

        north = extent['yMax']
        south = extent['yMin']
        east = extent['xMax']
        west = extent['xMin']

        outputRow = shpPath, extent['proj'], extent['yMax'], extent['yMin'], extent['xMax'], extent['xMin']

        f = open(weirdBBOut,'a')
        writer = csv.writer(f)

        if count == 0:
            writer.writerow(('Shapefile', 'Projection', 'North','South', 'East', 'West'))
            count +=1
        else:
            writer.writerow(outputRow)
        f.close

def processShapefile(shapeName, defaultPath = None, record = None, extraDir = None, option = None):
    outBoundingBox = os.path.join(shapeName[:-4]+'_BB.shp')
    outBoundingBoxVertices = os.path.join(shapeName[:-4]+'_BB_Vert.shp')

    #spatial_ref = arcpy.Describe(shapeName).spatialReference
    desc = arcpy.Describe(shapeName)
    try:
        spatial_ref = desc.SpatialReference
        projection = spatial_ref.name
        print 'Projection -', str(projection)
    except:
        projection = ''

    print 'Deleting BB if found'
    if arcpy.Exists(outBoundingBox):
        arcpy.Delete_management(outBoundingBox)
    if arcpy.Exists(outBoundingBoxVertices):
        arcpy.Delete_management(outBoundingBoxVertices)

    try:
        print 'Creating bounding box'
        # Use MinimumBoundingGeometry function to get an envelop area
        arcpy.MinimumBoundingGeometry_management(shapeName, outBoundingBox,
                                                 "ENVELOPE")

        print 'Convert vertices to points'
        # Convert vertices to points
        arcpy.FeatureVerticesToPoints_management(outBoundingBox, outBoundingBoxVertices, 'All')

        print 'Calculate X/Y for vertices'
        # Calculate X/Y for vertices
        arcpy.AddXY_management(outBoundingBoxVertices)

        xField = "Point_X"
        xMinValue = arcpy.SearchCursor(outBoundingBoxVertices, "", "", "", xField + " A").next().getValue(xField) #Get 1st row in ascending cursor sort
        xMaxValue = arcpy.SearchCursor(outBoundingBoxVertices, "", "", "", xField + " D").next().getValue(xField) #Get 1st row in descending cursor sort

        yField = "Point_Y"
        yMinValue = arcpy.SearchCursor(outBoundingBoxVertices, "", "", "", yField + " A").next().getValue(yField) #Get 1st row in ascending cursor sort
        yMaxValue = arcpy.SearchCursor(outBoundingBoxVertices, "", "", "", yField + " D").next().getValue(yField) #Get 1st row in descending cursor sort

    except:
        xMinValue = ''
        xMaxValue = ''
        yMinValue = ''
        yMaxValue = ''

    if arcpy.Exists(outBoundingBox):
        arcpy.Delete_management(outBoundingBox)
    if arcpy.Exists(outBoundingBoxVertices):
        arcpy.Delete_management(outBoundingBoxVertices)

    return {'xMin':xMinValue, 'xMax':xMaxValue,'yMin':yMinValue, 'yMax':yMaxValue, 'proj':projection}
    '''

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

def maxboundingbox(startDir):
    """ USE TO DETERMINE MAX BOUNDING BOX FOR DIRECTORY """

    xMin = ''
    xMax = ''
    yMin = ''
    yMax = ''

    for root, dirs, files in os.walk(startDir):
        for f in files:
            if f.endswith('.shp'):
                filePath = os.path.join(root, f)
                results = processShapefile(filePath)

                if xMin == '' or xMin > results['xMin']:
                    xMin = results['xMin']

                if xMax == '' or xMax < results['xMax']:
                    if results['xMax'] != '':
                        xMax = results['xMax']

                if yMin == '' or yMin > results['yMin']:
                    yMin = results['yMin']

                if yMax == '' or yMax < results['yMax']:
                    if results['yMax'] != '':
                        yMax = results['yMax']

                print xMin, xMax, yMin, yMax