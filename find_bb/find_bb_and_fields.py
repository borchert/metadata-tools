import arcpy
import os

def processShapefile(shapeName, record, extraDir):
    shpExt = shapeName+'.shp'
    record = record
    extraDir = extraDir
    defaultPath = r'D:\drive\Map Library Projects\MGS\Records\\'

    if extraDir == '':
        inlayer = os.path.join(defaultPath,record,shpExt)
        outBoundingBox = os.path.join(defaultPath,record,shapeName+'_BB.shp')
        outBoundingBoxVertices = os.path.join(defaultPath,record,shapeName+'_BB_Vert.shp')
    else:
        inlayer = os.path.join(defaultPath,record,extraDir,shpExt)
        outBoundingBox = os.path.join(defaultPath,record,extraDir,shapeName+'_BB.shp')
        outBoundingBoxVertices = os.path.join(defaultPath,record,extraDir,shapeName+'_BB_Vert.shp')

    print 'Deleting BB if found'
    if arcpy.Exists(outBoundingBox):
        arcpy.Delete_management(outBoundingBox)
    if arcpy.Exists(outBoundingBoxVertices):
        arcpy.Delete_management(outBoundingBoxVertices)

    print 'Creating bounding box'
    # Use MinimumBoundingGeometry function to get an envelop area
    arcpy.MinimumBoundingGeometry_management(inlayer, outBoundingBox,
                                             "ENVELOPE")

    print 'Convert vertices to points'
    # Convert vertices to points
    arcpy.FeatureVerticesToPoints_management (outBoundingBox, outBoundingBoxVertices, 'All'
    )

    # Calculate X/Y for vertices
    arcpy.AddXY_management(outBoundingBoxVertices)

    xField = "Point_X"
    xMinValue = arcpy.SearchCursor(outBoundingBoxVertices, "", "", "", xField + " A").next().getValue(xField) #Get 1st row in ascending cursor sort
    xMaxValue = arcpy.SearchCursor(outBoundingBoxVertices, "", "", "", xField + " D").next().getValue(xField) #Get 1st row in descending cursor sort

    yField = "Point_Y"
    yMinValue = arcpy.SearchCursor(outBoundingBoxVertices, "", "", "", yField + " A").next().getValue(yField) #Get 1st row in ascending cursor sort
    yMaxValue = arcpy.SearchCursor(outBoundingBoxVertices, "", "", "", yField + " D").next().getValue(yField) #Get 1st row in descending cursor sort

    if arcpy.Exists(outBoundingBox):
        arcpy.Delete_management(outBoundingBox)
    if arcpy.Exists(outBoundingBoxVertices):
        arcpy.Delete_management(outBoundingBoxVertices)

    return {'xMin':xMinValue, 'xMax':xMaxValue,'yMin':yMinValue, 'yMax':yMaxValue}


    print '---------------------\n'

def findFields(shapeName, record, extraDir):
    fieldDict = {}
    shpExt = shapeName+'.shp'
    record = record
    extraDir = extraDir
    defaultPath = r'D:\drive\Map Library Projects\MGS\Records\\'

    if extraDir == '':
        inlayer = os.path.join(defaultPath,record,shpExt)
    else:
        inlayer = os.path.join(defaultPath,record,extraDir,shpExt)

    fieldList = arcpy.ListFields(inlayer)

    for field in fieldList:
        fieldName = field.name
        fieldType = field.type
        fieldDict[fieldName] = fieldType

    return fieldDict


exitScript = ''
print 'Importing ArcPy takes forever, I know.'

while exitScript != 'x':

    shapeName = raw_input('Shapefile Name: ')
    record = raw_input("Record Number: ")
    extraDir = raw_input('Extra directory: ')

    extent = processShapefile(shapeName, record, extraDir)

    north = extent['yMax']
    south = extent['yMin']
    east = extent['xMax']
    west = extent['xMin']

    bbFile = r'D:/drive/Map Library Projects/MGS/Records/' + record + '/converted/' + shapeName + '_bb.txt'
    f = open(bbFile, 'w')
    boundingBoxOutput = ['North: ', str(north), '\nSouth: ', str(south), '\nEast: ', str(east), '\nWest: ', str(west)]
    f.write(''.join(boundingBoxOutput))
    f.close()

    fFields = findFields(shapeName, record, extraDir)
    fieldsFile = r'D:/drive/Map Library Projects/MGS/Records/' + record + '/converted/' + shapeName + '_fields.txt'
    f = open(fieldsFile, 'w')
    for key, value in fFields.items():
        fieldOut = key+'('+value+')\n'
        f.write(fieldOut)
    f.close()

    exitScript = raw_input("Press x to quit or enter to continue:   ")
