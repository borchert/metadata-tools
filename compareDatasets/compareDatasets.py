__author__ = 'mart3565'

''' --------------------------------------------------------------------

Script used to compare two paths for differences in files present (shp).

------------------------------------------------------------------------'''

import os
import arcpy

inputDirOne = r'C:\Users\mart3565\Downloads\hennepin'
inputDirTwo = r'C:\Users\mart3565\Downloads\hennepin11102014'

fileList = []
fileMatches = {}
fileDifferences = []
fieldList = []

def compareFileDir(dirOne, dirTwo):

    for root, dirs, files in os.walk(dirOne):
        for f in files:
            if f.endswith('.shp'):
                fileList.append(f)

                # Create default dictionary
                fileMatches.setdefault(f, [])

                # Add key (file) and value (root)
                fileMatches[f].append(root)

    for root, dirs, files in os.walk(dirTwo):
        for f in files:
            if f.endswith('.shp'):
                if f not in fileList:
                    #print 'Not present:',f

                    # Add to complete list of files
                    fileList.append(f)

                    # Add to list of different files
                    fileDifferences.append(os.path.join(root,f))
                else:
                    # Add second value (file root) to matching files
                    fileMatches[f].append(root)

def compareGeometry():
    for key, value in fileMatches.iteritems() :
        shapeOne = os.path.join(value[0], key)
        shapeTwo = os.path.join(value[1], key)

        fieldList = arcpy.ListFields(shapeOne)
        for field in fieldList:
           print("{0} is a type of {1} with a length of {2}".format(field.name, field.type, field.length))

        '''fieldList = arcpy.ListFields(shapeTwo)
        for field in fieldList:
            try:
                fieldName = str(field.name)
                #print("{0} is a type of {1} with a length of {2}".format(field.name, field.type, field.length))
                if fieldName not in fieldList:
                    fieldList.append(fieldName)
            except:
                pass'''
        #print shapeOne
        #print shapeTwo
        sort_field = 'FID'
        compare_type = "ALL"
        compare_result = arcpy.FeatureCompare_management(shapeOne,shapeTwo,sort_field,compare_type)

        print 'Compared results:',compare_result[0]


compareFileDir(inputDirOne,inputDirTwo)

#print fileMatches
#compareGeometry()