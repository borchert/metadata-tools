import arcpy
import os.path, os,fnmatch
import time
import pdb
import glob

#Get the record and path to XMLs
record = raw_input("Enter record number: ")
record_path = raw_input("Enter path to shapefiles: ")
blankMXD = r'D:\drive\Map Library Projects\MGS\Metadata Templates\blank.mxd'

#Static vars
TRANSLATOR = "C:\\Program Files\\ArcGIS\\Desktop10.2\\Metadata\\Translator\\ARCGIS2FGDC.xml"
base_path = "D:\\drive\\Map Library Projects\\MGS\\Records"

#set workspace
arcpy.env.workspace = os.path.join(base_path, record, record_path)
ws = arcpy.env.workspace

#create final_XMLs dir if it doesn't already exist
if os.path.exists(os.path.join(base_path,record,"final_XMLs")) == False:
    arcpy.CreateFolder_management(os.path.join(base_path,record),"final_XMLs")

#set the output path for export metadata function
OUTPUT = os.path.join(base_path,record,"final_XMLs")

def import_XML():

    importXMLpath = raw_input("Enter path to XML template: ")
    
    importXMLpath = importXMLpath.replace('"','')
    
    #get a list of all the SHPs
    if record_path == "converted\GISfiles":
        files = []
        for dirpath,dirnames,filenames in os.walk(os.path.join(base_path,record,record_path)):
            if dirpath.endswith("shapefiles"):
                for f in filenames:
                    if fnmatch.fnmatch(f,"*.shp"):
                        files.append(os.path.join(dirpath,f))
                    
    else:
        files = glob.glob(os.path.join(arcpy.env.workspace,"*.shp"))

    totalTimeTic = time.time()

    #loop through SHPs and import the metadata for each
    for f in files:

        #shapefilePath = os.path.join(base_path,record,record_path,f)

        tic = time.time()
        print 'Trying to import XML to: ', f
        arcpy.ImportMetadata_conversion (importXMLpath,"FROM_FGDC",f, "DISABLED")

        '''# get the map document
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
        mxd.save()'''

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
    if record_path == "converted\GISfiles":
        files = []
        for dirpath,dirnames,filenames in os.walk(os.path.join(base_path,record,record_path)):
            if dirpath.endswith("shapefiles"):
                for f in filenames:
                    if fnmatch.fnmatch(f,"*.xml"):
                        files.append(os.path.join(dirpath,f))
    else:
         files = glob.glob(os.path.join(arcpy.env.workspace,"*.shp"))


    #loop through XMLs and export the metadata for each to the final_XMLs directory
    for f in files:

        
        if os.path.splitext(f)[1] == '.shp':
            if os.path.isabs(f) == False:
                filePath = os.path.join(OUTPUT,
                    os.path.split(os.path.splitext(f)[0])[1],'.xml')
            else:
                filePath = os.path.join(OUTPUT,os.path.split(f)[1])
        elif f[len(f)-7:len(f)-4] == 'txt':
            pass
        else:
            if os.path.isabs(f) == False:
                filePath = os.path.join(OUTPUT,f)
            else:
                filePath = os.path.join(OUTPUT,os.path.split(f)[1])

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
