import arcpy
import os

def getDrivePath():
    while True:
        drivePath = raw_input("Please enter the path to your Drive folder (i.e. D:\drive or C:\Users\username\Google "
                              "Drive):  ")
        if not os.path.exists(drivePath):
            print 'That path does not work.  Please try again.'
        else:
            break
    return drivePath

def processShapefile(shapeName, defaultPath, record, extraDir, option = None):

    if option == 0:
        pass
    elif option == 1:
        shapeName = validateInput("shapeName", "Shapefile name: ", defaultPath, record, extraDir)
    else:
        record = validateInput("record","Record Number: ", defaultPath)
        extraDir = validateInput("extraDir", "Extra directory: ", defaultPath, record)
        shapeName = validateInput("shapeName", "Shapefile name: ", defaultPath, record, extraDir)

    shpExt = shapeName+'.shp'

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

def findFields(shapeName, defaultPath, record, extraDir):
    fieldDict = {}
    shpExt = shapeName+'.shp'
    record = record
    extraDir = extraDir

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

def validateInput(type, msg, defaultPath, record = None, extraDir = None):
    val = raw_input(msg)
    if type == 'record':
        valDir = os.path.join(defaultPath,val)
        error = 'That record number doesn\'t exist.  Please try again.\n'
    if type == 'extraDir':
        valDir = os.path.join(defaultPath,record,val)
        error = 'That extra directory doesn\'t exist. Please try again.\n'
    if type == 'shapeName':
        val += '.shp'
        valDir = os.path.join(defaultPath,record,extraDir, val)
        error = 'That shapefile doesn\'t exist. Please try again.\n'

    while True:
        try:
            print valDir
            if not os.path.exists(valDir):
                print error
                val = raw_input(msg)
                if type == 'record':
                    valDir = os.path.join(defaultPath,val)

                if type == 'extraDir':
                    valDir = os.path.join(defaultPath,record,val)

                if type == 'shapeName':
                    val += '.shp'
                    valDir = os.path.join(defaultPath,record,extraDir,val)

            else:
                break
        except:
            break
    if val.endswith('.shp'):
        return val[:-4]
    else:
        return val


print 'Importing ArcPy takes forever, I know.'

userName = os.environ.get('USERNAME')

# Find location of Drive path
if os.path.exists(r'D:\drive\\'):
    defaultPath = r'D:\drive\Map Library Projects\MGS\Records\\'
elif os.path.exists(os.path.join(r'C:\Users\\',userName,'Google Drive')):
    defaultPath = os.path.join(r'C:\Users\\',userName,'Google Drive\Map Library Projects\MGS\Records\\')
else:
    getDrivePath()


record = validateInput("record","Record Number: ", defaultPath)
extraDir = validateInput("extraDir", "Extra directory: ", defaultPath, record)
shapeName = validateInput("shapeName", "Shapefile name: ", defaultPath, record, extraDir)

while True:

    extent = processShapefile(shapeName, defaultPath, record, extraDir, 0)

    north = extent['yMax']
    south = extent['yMin']
    east = extent['xMax']
    west = extent['xMin']

    bbFile = defaultPath + record + '/converted/' + shapeName + '_bb.txt'
    f = open(bbFile, 'w')
    boundingBoxOutput = 'North: ', str(north), '\nSouth: ', str(south), '\nEast: ', str(east), '\nWest: ', str(west), '\n'
    print 'Writing bounding box text file.'
    for x in boundingBoxOutput:
        f.write(x)
    print 'Closing bounding box text file.'
    f.close()

    fFields = findFields(shapeName, defaultPath, record, extraDir)
    fieldsFile = defaultPath + record + '/converted/' + shapeName + '_fields.txt'
    f = open(fieldsFile, 'w')
    print 'Writing fields text file.'
    for key, value in fFields.items():
        fieldOut = key+'('+value+')\n'
        f.write(fieldOut)
    print 'Closing fields text file.\n'
    print '---------------------------\n'
    f.close()

    exitScript = raw_input("Press x to quit, n to enter a new record, or enter to continue with same inputs:   ")
    print '\n'

    if exitScript in ('x', 'X'):
        break
    elif exitScript in ('n', 'N'):
        processShapefile(shapeName, defaultPath, record, extraDir)
    else:
        processShapefile(shapeName, defaultPath, record, extraDir, option=1)










