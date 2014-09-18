# defining projections that are Unknown. Sets those to the most frequent SRS for the record. 99% of them are UTM 15N anyways.

import arcpy
import os.path
import os
import sys
from pprint import pprint
import pdb

records = [108814,109019,116056,116097,123383,167,191,203,210,290,306,310,321,406,414,422,432,440,514,518,56995,56997,57000,57002,57004,57172,57174,57177,57178,57181,57182,57186,57241,57242,57440,57694,57695,57699,57702,58041,58042,58162,58164,58165,58175,58233,58513,58549,58551,58554,58560,58716,58719,58781,58804,59648,59765,59783,59784,604,928,92939,92941,936,973,98055]
ROOT = ""

install_dir = arcpy.GetInstallInfo("desktop")["InstallDir"]
translator = os.path.join(install_dir,  "Metadata\Translator\ARCGIS2FGDC.xml")

for i in records:
    unknowns = []
    srs = {}
    
    #ws = os.path.join(ROOT,str(i),"converted","GISfiles")
    ws = os.path.join(ROOT,str(i))
    xml_path = os.path.join(ROOT,str(i),"final_XMLs")
    walk = arcpy.da.Walk(ws,datatype=["FeatureClass","RasterDataset"])

    if not os.path.exists(os.path.join(ws,"converted","GISfiles")):   
        for dirpath,dirname,files in walk:
            for f in files:
                d = os.path.join(dirpath,f)
                desc = arcpy.Describe(d)
                if desc.datatype.startswith('ShapeFile'):
                    if desc.spatialreference:
                        sr = desc.spatialreference.PCSCode
                        if sr == 0:
                            unknowns.append(d)
                        if srs.has_key(sr):
                            srs[sr] = srs[sr] + 1
                        else:
                            srs[sr] = 1
                    else:
                        print f,'has no spatial ref'
                    
                    
        #see https://wiki.python.org/moin/HowTo/Sorting for more on sorting iterables
        most_popular_srs = sorted(srs.iteritems(), reverse=True, key=lambda item: item[1])[0][0]

        #create spatial reference object using the code
        new_srs = arcpy.SpatialReference(most_popular_srs)
        print new_srs.name,'is the most popular SRS for', i

    else:
        print 'skipped %s because it has e00s' % (str(i))
        
    for d in unknowns:
        arcpy.DefineProjection_management(d, new_srs)
        print 'defined projection for' ,d

        path_to_xml = os.path.join(xml_path, os.path.split(d)[1]+".xml")
        if os.path.exists(path_to_xml):
            os.remove(path_to_xml)
            print 'removed existing XML to make room for a new one'
        arcpy.ExportMetadata_conversion(d, translator,
                                        path_to_xml)
        print 'exported new XML for', d

    print '\n'


                                        

