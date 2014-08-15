import arcpy
import os.path

#Get the record and path to XMLs
record = raw_input("Enter record number: ")
record_path = raw_input("Enter path to shapefiles: ")

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

#get a list of all the XMLs
files = arcpy.ListFiles("*.xml")
print files

#loop through XMLs and export the metadata for each to the final_XMLs directory
for f in files:
    arcpy.ExportMetadata_conversion(f,
        TRANSLATOR,
        os.path.join(OUTPUT, f[:f.find(".")]+ ".xml")
    )
