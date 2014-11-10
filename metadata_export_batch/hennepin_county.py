import find_Drive
import os
import arcpy

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
    outDir = os.path.join(input_path, 'export_fgdc')
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    for root, dirs, files in os.walk(input_path):
        for f in files:
            if f.endswith('shp'):
                inFile = os.path.join(root, f)
                outFile = os.path.join(outDir,(f[:-4]+'.xml'))
                ws = os.path.join(root)
                if os.path.isfile(outFile):
                    print 'Removing', outFile
                    os.remove(outFile)

                print 'Trying to export XML for: ', f
                arcpy.ExportMetadata_conversion(inFile, translator, outFile)

drivePath = find_Drive.main()

importPath = r'C:\Users\mart3565\Downloads\hennepin11102014'

translator = "C:\\Program Files\\ArcGIS\\Desktop10.2\\Metadata\\Translator\\ARCGIS2FGDC.xml"

export_xml(importPath)
