# defining projections that are Unknown. Sets those to the most frequent SRS for the record. 99% of them are UTM 15N anyways.

import arcpy
import os.path
import os
import sys
from pprint import pprint
import pdb

e00s = [317,321,406,414,422,
           432,440,514,518,600,
           604,928,936,56995,56996,
           56997,57000,57002,57004,
           57172,57186]


ROOT = ''

install_dir = arcpy.GetInstallInfo("desktop")["InstallDir"]
translator = os.path.join(install_dir,  "Metadata\Translator\ARCGIS2FGDC.xml")

for i in e00s[0:1]:
    unknowns = []
    srs = {}
    
    ws = os.path.join(ROOT,str(i),"converted","GISfiles")
    xml_path = os.path.join(ROOT,str(i),"final_XMLs")
    walk = arcpy.da.Walk(ws,datatype=["FeatureClass","RasterDataset"])

    for dirpath,dirname,files in walk:
        for f in files:
            d = os.path.join(dirpath,f)
            desc = arcpy.Describe(d)
            if desc.datatype.startswith('ShapeFile'):
                if desc.spatialreference:
                    sr = desc.spatialreference.PCSCode
                    if sr == 0:
                        unknowns.append(d)
                else:
                    print f,'has no spatial ref'
                if srs.has_key(sr):
                    srs[sr] = srs[sr] + 1
                else:
                    srs[sr] = 1
                    
    #see https://wiki.python.org/moin/HowTo/Sorting for more on sorting iterables
    most_popular_srs = sorted(srs.iteritems(), reverse=True, key=lambda item: item[1])[0][0]
    new_srs = arcpy.SpatialReference(most_popular_srs)
    print new_srs.name,'is the most popular SRS for', i
    
    for d in unknowns:
        arcpy.DefineProjection_management(d, new_srs)
        print 'defined projection for' ,d

        path_to_xml = os.path.join(xml_path, os.path.split(d)[1]+".xml")
        if os.path.exists(path_to_xml):
            os.remove(path_to_xml)
            print 'removed existing XML to make room for a new one'
        arcpy.ExportMetadata_conversion(d, translator,
                                        path_to_xml)
        print 'exported new XML for', d,'\n'


                                        
