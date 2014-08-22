__author__ = 'mart3565'
import arcpy
import os.path
import time

def getDrivePath():
    while True:
        drivePath = raw_input("Please enter the path to your Drive folder (i.e. D:\drive or C:\Users\username\Google "
                              "Drive):  ")
        if not os.path.exists(drivePath):
            print 'That path does not work.  Please try again.'
        else:
            break
    return drivePath

userName = os.environ.get('USERNAME')

if os.path.exists(r'D:\drive\\'):
    drivePath = r'D:\drive\Map Library Projects\MGS'
elif os.path.exists(os.path.join(r'C:\Users\\',userName,'Google Drive')):
    drivePath = os.path.join(r'C:\Users\\',userName,'Google Drive\Map Library Projects\MGS')
else:
    drivePath = getDrivePath()

#Get the record and path to XMLs
record = raw_input("Enter record number: ")
record_path = raw_input("Enter path to shapefiles: ")
blankMXD = r'D:\drive\Map Library Projects\MGS\Metadata Templates\blank.mxd'

#Static vars
TRANSLATOR = "C:\\Program Files\\ArcGIS\\Desktop10.2\\Metadata\\Translator\\ARCGIS2FGDC.xml"
ISOTRANSLATOR = "C:\\Program Files\\ArcGIS\\Desktop10.2\\Metadata\\Translator\\ARCGIS2ISO19139.xml"
base_path = os.path.join(drivePath,"Records")

#set workspace
arcpy.env.workspace = os.path.join(base_path, record, record_path)
ws = arcpy.env.workspace

#create final_XMLs dir if it doesn't already exist
if os.path.exists(os.path.join(base_path,record,"final_XMLs")) == False:
    arcpy.CreateFolder_management(os.path.join(base_path,record),"final_XMLs")

#set the output path for export metadata function
OUTPUT = os.path.join(base_path,record,"final_XMLs")

def import_XML():

    baseSHP = raw_input('Enter shapefile to use as template: ')
    shpPath = os.path.join(base_path, record,record_path,baseSHP)
    templatePath = os.path.join(base_path,record,'final_XMLs\template\template.xml')
    print shpPath

    arcpy.ExportMetadata_conversion (shpPath, ISOTRANSLATOR,
    templatePath)

    #get a list of all the SHPs
    files = arcpy.ListFiles("*.shp")

    totalTimeTic = time.time()

    #loop through SHPs and import the metadata for each
    for f in files:

        shapefilePath = os.path.join(base_path,record,record_path,f)

        tic = time.time()
        print 'Trying to import XML to: ', f
        arcpy.ImportMetadata_conversion (templatePath,"FROM_ESRIISO",f, "DISABLED")

        # Trying to get thumbnail, postponing for now.
        """# get the map document
        mxd = arcpy.mapping.MapDocument(blankMXD)
        # get the data frame
        df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
        # create a new layer
        newlayer = arcpy.mapping.Layer(shapefilePath)
        # add the layer to the map at the bottom of the TOC in data frame 0
        arcpy.mapping.AddLayer(df, newlayer,"BOTTOM")
        print "creating thumbnail for " + f
        mxd.makeThumbnail()
        mxd.save()
        arcpy.mapping.RemoveLayer(df, newlayer)
        mxd.save()"""

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

def export_xml():
    #set the output path for export metadata function
    OUTPUT = os.path.join(base_path,record,"final_XMLs")

    #get a list of all the XMLs
    files = arcpy.ListFiles("*.xml")
    print files

    #loop through XMLs and export the metadata for each to the final_XMLs directory
    for f in files:

        if f[len(f)-7:len(f)-4] == 'shp':
            filePath = os.path.join(OUTPUT,f[:-8]+'.xml')
        elif f[len(f)-7:len(f)-4] == 'txt':
            pass
        else:
            filePath = os.path.join(OUTPUT,f)

        print filePath

        statinfo = os.stat(os.path.join(base_path,record,record_path,f))

        print f, '=', statinfo.st_size

        if statinfo.st_size == 0:
            continue

        if os.path.exists(filePath):
            print f, 'already exists.  Deleting now.'
            os.remove(filePath)

        print 'Trying to export XML for: ', f
        arcpy.ExportMetadata_conversion(f,
            TRANSLATOR,
            os.path.join(OUTPUT, f[:f.find(".")]+ ".xml"))


imp_xml = raw_input('Do you want to batch import XML? ')
if imp_xml.lower() in ('yes', 'y'):
    import_XML()

exp_xml = raw_input('Do you want to batch export XML? ')
if exp_xml.lower() in ('yes','y'):
    export_xml()