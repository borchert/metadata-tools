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

    if option == 0:
        pass
    elif option == 1:
        importE00File = validateInput("e00Name", "E00 name: ", defaultPath, record, extraDir)
    else:
        record = validateInput("record","Record Number: ", defaultPath)
        extraDir = validateInput("extraDir", "Extra directory: ", defaultPath, record)
        importE00File = validateInput("e00Name", "E00 name: ", defaultPath, record, extraDir)

    if importE00File.endswith('.e00'):
        e00Ext = importE00File
    else:
        e00Ext = importE00File + '.e00'

    if extraDir == '':
        envDir = os.path.join(defaultPath,record)
    else:
        envDir = os.path.join(defaultPath,record,extraDir)

    outDirectory = os.path.join(defaultPath, record + '\converted\GISfiles', importE00File[:-4])

    outName = str(e00Ext[:-4])

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
            print 'inFeatures -', inFeatures

            outLocation = outDirectory + "\\shapefiles"
            print 'outLocation -', outLocation

            if os.path.exists(outLocation):
                pass
            else:
                os.makedirs(outLocation)
                print 'Created: ' + str(outLocation)

            outFeatureClass = importE00File + '_' + x + ".shp"
            print 'outFeatureClass - ', outFeatureClass

            errorLog = outDirectory + '\_errorLog.txt'

            try:
                # Execute FeatureClassToFeatureClass
                arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation,
                                                            outFeatureClass)

            except:
                e = open(errorLog, 'a')
                error = [x, '- could not convert to SHP']
                e.write(''.join(error))
                e.close()

            try:
                featureCount = arcpy.GetCount_management(x)
            except:
                e = open(errorLog, 'a')
                error = [x, '- could not count features']
                e.write(''.join(error))
                e.close()

            featureCountFile = outDirectory + '\_featureCount.txt'
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
                    val += '.e00'
                    valDir = os.path.join(defaultPath,record,extraDir,val)

            else:
                break
        except:
            break
    if val.endswith('.e00'):
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

