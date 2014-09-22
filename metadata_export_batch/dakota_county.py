import find_Drive
import os
import arcpy
from arcpy import env

def import_XML():

    templatePath = outputXML
    totalTimeTic = time.time()
    print 'Full path - ', fullPath

    #loop through SHPs and import the metadata for each
    failedMetaImport = []
    for root, dirs, files in os.walk(fullPath):

        dirname = root.split(os.path.sep)[-1]

        #set workspace
        arcpy.env.workspace = os.path.join(defaultPath, record, dirname)
        ws = arcpy.env.workspace

        #print ws

        for f in files:

            if f.lower().endswith('.shp'):
                tic = time.time()
                print 'Trying to import XML to: ', f
                print templatePath
                try:
                    arcpy.ImportMetadata_conversion(templatePath, "FROM_FGDC", f, "DISABLED")
                except:
                    failedMetaImport.append(f)
                toc = time.time()
                s = toc-tic
                m, s = divmod(s, 60)
                h, m = divmod(m, 60)
                timeFormat = "%d:%02d:%02d" % (h, m, s)
                print 'Time elapsed: ',timeFormat

    totalTimeToc = time.time()
    s = totalTimeToc-totalTimeTic
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    timeFormat = "%d:%02d:%02d" % (h, m, s)
    print 'Total time elapsed: ',timeFormat

def export_xml(input_path):

    for root, dirs, files in os.walk(input_path):
        for f in files:
            if f.endswith('shp'):
                inFile = os.path.join(root, f)
                outFile = os.path.join(outputDir,f[:-4]+'.xml')
                print outFile
                if os.path.isfile(outFile):
                    print 'Removing', outFile
                    os.remove(outFile)

                print 'Trying to export XML for: ', f
                arcpy.ExportMetadata_conversion(inFile, translator, outFile)

def export_SHP_from_GDB(input_path):
    for root, dirs, files in os.walk(importPath):
        for d in dirs:
            if d.endswith('.gdb'):
                print 'Working on -', d
                env.workspace = os.path.join(root, d)
                fcList = arcpy.ListFeatureClasses()
                outDirectory = os.path.join(root,'shapefiles')
                print outDirectory
                if not os.path.isdir(outDirectory):
                    os.mkdir(outDirectory)
                    print 'Created -', outDirectory
                #for feature in fcList:
                arcpy.FeatureClassToShapefile_conversion(fcList, outDirectory)


drivePath = find_Drive.main()

todo = [r'C:\Users\mart3565\Downloads\Dakota\Apple Valley\shapefiles', r'C:\Users\mart3565\Downloads\Dakota\Burnsville\shapefiles', r'C:\Users\mart3565\Downloads\Dakota\Eagan\shapefiles', r'C:\Users\mart3565\Downloads\Dakota\Farmington\shapefiles', r'C:\Users\mart3565\Downloads\Dakota\Hastings\shapefiles', r'C:\Users\mart3565\Downloads\Dakota\Inver Grove Heights\shapefiles', r'C:\Users\mart3565\Downloads\Dakota\Lakeville\shapefiles',r'C:\Users\mart3565\Downloads\Dakota\Mendota, Mendota Heights & Lilydale\shapefiles',r'C:\Users\mart3565\Downloads\Dakota\Rosemount\shapefiles', r'C:\Users\mart3565\Downloads\Dakota\South St. Paul\shapefiles', r'C:\Users\mart3565\Downloads\Dakota\West St. Paul\shapefiles']
#importPath = r'C:\Users\mart3565\Downloads\Dakota'
outputDir = os.path.join(drivePath,'metadata\sources\dakota-county\exported_fgdc')
translator = "C:\\Program Files\\ArcGIS\\Desktop10.2\\Metadata\\Translator\\ARCGIS2FGDC.xml"

if not os.path.isdir(outputDir):
    os.mkdir(outputDir)
    print 'Created -', outputDir

for x in todo:
    importPath = x
    #print importPath
    export_xml(importPath)