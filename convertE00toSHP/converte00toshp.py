import arcpy
from arcpy import env
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

def convertE00toShapefile(importE00File, defaultPath, record, extraDir, option=None):

    print importE00File

    if option == 0:
        pass
    elif option == 1:
        importE00File = validateInput("e00Name", "E00 name: ", defaultPath, record, extraDir)
    else:
        record = validateInput("record","Record Number: ", defaultPath)
        extraDir = validateInput("extraDir", "Extra directory: ", defaultPath, record)
        importE00File = validateInput("e00Name", "E00 name: ", defaultPath, record, extraDir)

    print importE00File

    if importE00File.endswith('.e00'):
        e00Ext = importE00File
    else:
        e00Ext = importE00File + '.e00'

    if extraDir == '':
        envDir = os.path.join(defaultPath,record)
    else:
        envDir = os.path.join(defaultPath,record,extraDir)

    outDirectory = os.path.join(defaultPath, record + '\converted\GISfiles', importE00File[:-4])
    print outDirectory

    outName = str(importE00File[:-4])

    print outName

    # Set environment settings
    if os.path.exists(outDirectory):
        pass
    else:
        os.makedirs(outDirectory)
        print 'Created: ' + str(outDirectory)

    env.workspace = envDir
    env.overwriteOutput = True

    # Delete pre-existing output
    if env.overwriteOutput:
        if os.path.exists(outName):
            os.remove(outName)

    # Execute ImportFromE00
    arcpy.ImportFromE00_conversion(e00Ext, outDirectory, outName)

    envDir = os.path.join(defaultPath,record + '\converted\GISfiles', importE00File[:-4], outName)
    env.workspace = envDir
    fc = arcpy.ListFeatureClasses()

    for x in fc:
        if x[:10] != 'annotation':
            # Set local variables
            inFeatures = os.path.join(outDirectory,outName,x)
            outLocation = outDirectory + "\\shapefiles"

            print '67'

            if os.path.exists(outLocation):
                pass
            else:
                os.makedirs(outLocation)
                print 'Created: ' + str(outLocation)

            print '73'

            outFeatureClass = importE00File + '_' + x + ".shp"

            print '77'

            # Execute FeatureClassToFeatureClass
            arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation,
                                                        outFeatureClass)

            featureCount = arcpy.GetCount_management(x)

            featureCountFile = outLocation + 'featureCount.txt'
            f = open(featureCountFile, 'a')
            writeOutput = str(x)+' - '+ str(featureCount)+' features\n'
            f.write(writeOutput)

    f.close()
    print 'Complete\n-------------------------\n'


def validateInput(type, msg, defaultPath, record = None, extraDir = None):
    val = raw_input(msg)
    if type == 'record':
        valDir = os.path.join(defaultPath,val)
        error = 'That record number doesn\'t exist.  Please try again.\n'
    if type == 'extraDir':
        valDir = os.path.join(defaultPath,record,val)
        error = 'That extra directory doesn\'t exist. Please try again.\n'
    if type == 'e00Name':
        val += '.e00'
        valDir = os.path.join(defaultPath,record,extraDir, val)
        error = 'That e00 file doesn\'t exist. Please try again.\n'

    while True:
        try:
            if not os.path.exists(valDir):
                print error
                val = raw_input(msg)
                if type == 'record':
                    valDir = os.path.join(defaultPath,val)

                if type == 'extraDir':
                    valDir = os.path.join(defaultPath,record,val)

                if type == 'e00Name':
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

# Set local variables
userName = os.environ.get('USERNAME')

if os.path.exists(r'D:\drive\\'):
    defaultPath = r'D:\drive\Map Library Projects\MGS\Records\\'
elif os.path.exists(os.path.join(r'C:\Users\\',userName,'Google Drive')):
    defaultPath = os.path.join(r'C:\Users\\',userName,'Google Drive\Map Library Projects\MGS\Records\\')
else:
    getDrivePath()

record = validateInput("record","Record Number: ", defaultPath)
extraDir = validateInput("extraDir", "Extra directory: ", defaultPath, record)
importE00File = validateInput("e00Name", "E00 name: ", defaultPath, record, extraDir)

convertE00toShapefile(importE00File, defaultPath, record, extraDir, option=0)

while True:

    exitScript = raw_input("Press x to quit, n to enter a new record, or enter to continue with same inputs:   ")
    print '\n'
    print '--------------------\n'

    if exitScript in ('x', 'X'):
        break
    elif exitScript in ('n', 'N'):
        convertE00toShapefile(importE00File, defaultPath, record, extraDir)
    else:
        convertE00toShapefile(importE00File, defaultPath, record, extraDir, option = 1)

