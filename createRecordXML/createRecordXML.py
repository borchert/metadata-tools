import urllib2
import os.path
import operator
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import arcpy
import time
import glob

def getDrivePath():
    while True:
        drivePath = raw_input("Please enter the path to your Drive folder (i.e. D:\drive or C:\Users\username\Google "
                              "Drive):  ")
        if not os.path.exists(drivePath):
            print 'That path does not work.  Please try again.'
        else:
            break
    return drivePath

def import_XML():

    passed = 1
    templatePath = outputXML
    #get a list of all the SHPs
    #files = arcpy.ListFiles("*.shp")

    totalTimeTic = time.time()
    print 'Full path - ', fullPath

    #loop through SHPs and import the metadata for each
    failedMetaImport = []
    for root, dirs, files in os.walk(fullPath):

        #dirname = root.split(os.path.sep)[-1]

        for f in files:

            if f.lower().endswith('.shp'):
                #set workspace
                arcpy.env.workspace = root
                ws = arcpy.env.workspace
                tic = time.time()
                print 'Trying to import XML to: ', f
                print templatePath
                try:
                    arcpy.ImportMetadata_conversion(templatePath, "FROM_FGDC", f, "DISABLED")
                except:
                    print 'Import failed.'
                    failedMetaImport.append(f)
                    passed = 0
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

    failedOutput = os.path.join(fullPath,'failedImport.txt')
    f = open(failedOutput,'w')
    for x in failedMetaImport:
        f.write(x)
        f.write('\n')
    f.close()
    return passed

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def keeper_attr(type):
    web = 'web' + type
    XML = 'XML' + type

    webAttr = globals()[web].strip()
    XMLAttr = globals()[XML].strip()
    if webAttr == '':
        keeper = XMLAttr
        print 'The XML metadata was kept by default because no web metadata was found.\n'
        print keeper
        validate = raw_input('Press enter to accept this value or enter a manual value.\n')
        if validate != '':
            keeper = validate
    elif XMLAttr == '':
        keeper = webAttr
        print 'The web metadata was kept by default because no XML metadata was found.\n'
        print type, '-', keeper, '\n'
        validate = raw_input('Press enter to accept this value or enter a manual value.\n')
        if validate != '':
            keeper = validate
    else:
        print 'A) Web',type,'= ', webAttr
        print 'B) XML',type,'= ', XMLAttr
        print 'C) Manually enter', type.lower()

        choice = raw_input('Please select A, B, or C as the '+ type.lower()+' to keep.\n')

        if choice in ['A', 'a']:
            keeper = webAttr
        elif choice in ['B','b']:
            keeper = XMLAttr
        else:
            keeper = raw_input('Enter the manual information:\n')

        print 'You chose to keep: ', keeper, '\n\n----------\n'

    return keeper

userName = os.environ.get('USERNAME')

if os.path.exists(r'D:\drive\\'):
    drivePath = r'D:\drive\Map Library Projects\MGS'
elif os.path.exists(os.path.join(r'C:\Users\\',userName,'Google Drive')):
    drivePath = os.path.join(r'C:\Users\\',userName,'Google Drive\Map Library Projects\MGS')
else:
    drivePath = getDrivePath()

inputTemplatePath = os.path.join(drivePath,'template.xml')

links = r'c:/users/chris/desktop/links.csv'

f = open(links)

content = f.readlines()
contentStripped = []
for x in content:
    contentStripped.append(x[:-1])

completeXML = r'c:/users/chris/desktop/completeXML.txt'
incompleteXML = r'c:/users/chris/desktop/incompleteXML.txt'

for item in contentStripped:
    link = item
    print link

    #Get the record and path to XMLs
    # Catch 5 digit records
    if len(link)==46:
        if link[len(link)-1]== '/':
            record = str(link[len(link)-6:len(link)-1])
        else:
            record = str(link[len(link)-6:len(link)])
    # Catch 4 digit records
    elif len(link)==45:
        if link[len(link)-1]== '/':
            record = str(link[len(link)-5:len(link)-1])
        else:
            record = str(link[len(link)-5:len(link)])
    # Catch 3 digit records
    elif len(link)==44:
        if link[len(link)-1]== '/':
            record = str(link[len(link)-4:len(link)-1])
        else:
            record = str(link[len(link)-4:len(link)])
    # Catch 6 digit records
    else:
        if link[len(link)-1]== '/':
            record = str(link[len(link)-7:len(link)-1])
        else:
            record = str(link[len(link)-7:len(link)])

    print 'Record number: ',record
    recordCheck = raw_input('Enter the correct record if the auto-generated record is incorrect')
    if len(recordCheck) >= 2:
        record = recordCheck
        print 'Record number: ',record

    #Static vars
    ISOTRANSLATOR = r"C:\Program Files\ArcGIS\Desktop10.2\Metadata\Translator\ArcGIS2FGDC.xml"
    defaultPath = os.path.join(drivePath,"Records")
    fullPath = os.path.join(defaultPath,record)
    convertedPath = os.path.join(fullPath,'converted')

    #create final_XMLs dir if it doesn't already exist
    if os.path.exists(os.path.join(fullPath ,"final_XMLs")) == False:
        arcpy.CreateFolder_management(fullPath,"final_XMLs")

    page = urllib2.urlopen(link).read()
    webSoup = BeautifulSoup(page)

    webTitle = webSoup.find("meta", {"name":"DC.title"})['content']
    try:
        webKeywords = webSoup.find_all("meta", {"name":"DC.subject"})
    except:
        webKeywords = ''
    try:
        webAbstract = webSoup.find("meta", {"name":"DCTERMS.abstract"})['content']
    except:
        webAbstract = ''
    try:
        webPurpose = webSoup.find("meta", {"name":"DC.description"})['content']
    except:
        webPurpose = ''
    try:
        webDate = webSoup.find("meta", {"name":"DCTERMS.issued"})['content']
    except:
        webDate = ''

    keyWordsList = []

    for x in webKeywords:
        keyWordsList.append(x.attrs['content'])

    webKeywordsHolder = []
    holder = ''

    for x in keyWordsList:
        holder += x

    webKeywords = holder.strip()

    # Print tree structure of files
    #list_files(convertedPath)

    XMLDict = {}
    for filename in os.listdir(convertedPath):
        if not filename.endswith('.xml'): continue
        filePath = os.path.join(convertedPath,filename)
        statinfo = os.stat(filePath)

        size = statinfo.st_size

        XMLDict[filename] = size

    try:
        largestXML = max(XMLDict.iteritems(), key=operator.itemgetter(1))[0]

        largestXMLPath = os.path.join(convertedPath, largestXML)

        f = open(largestXMLPath,'r')

        XMLsoup = BeautifulSoup(f)

        XMLFindTitle = XMLsoup.find_all("title")
        XMLTitle = ''

        for x in XMLFindTitle:
            if XMLTitle == '':
                XMLTitle = x.text

        XMLFindAbs = XMLsoup.find_all("abstract")
        XMLAbstract = ''

        for x in XMLFindAbs:
            if XMLAbstract == '':
                XMLAbstract = x.text

        XMLFindPurpose = XMLsoup.find_all("purpose")
        XMLPurpose = ''

        for x in XMLFindPurpose:
            if XMLPurpose == '':
                XMLPurpose = x.text

        XMLFindDate = XMLsoup.find_all("pubdate")
        XMLDate = ''

        for x in XMLFindDate:
            if XMLDate == '':
                XMLDate = x.text

        XMLFindThemeKey = XMLsoup.find_all("themekey")
        XMLFindPlaceKey = XMLsoup.find_all("placekey")
        XMLKeywordsHolder = []
        holder = ''

        for x in XMLFindThemeKey:
            XMLKeywordsHolder.append(x.text)

        for x in XMLFindPlaceKey:
            XMLKeywordsHolder.append(x.text)

        for x in XMLKeywordsHolder:
            holder += x

        XMLKeywords = holder.strip()

        XMLFindLineage = XMLsoup.find_all("lineage")
        XMLLineage = ''

        for x in XMLFindLineage:
            if XMLLineage == '':
                XMLLineage = x.text

        XMLFindHorizontalPosAccr = XMLsoup.find_all("horizpar")
        XMLHorizontalPosAccr = ''

        for x in XMLFindHorizontalPosAccr:
            if XMLHorizontalPosAccr == '':
                XMLHorizontalPosAccr = x.text

        XMLFindLinkage = XMLsoup.find_all("onlink")
        XMLLinkage = ''

        for x in XMLFindLinkage:
            if XMLLinkage == '':
                XMLLinkage = x.text

        #print XMLsoup.prettify()

    except:
        print 'No XML was found.'
        XMLAbstract = ''
        XMLDate = ''
        XMLHorizontalPosAccr = ''
        XMLKeywords = ''
        XMLLineage = ''
        XMLLinkage = ''
        XMLPurpose = ''
        XMLTitle = ''

    keeperTitle = keeper_attr('Title')
    keeperAbs = keeper_attr('Abstract')
    keeperPurpose = keeper_attr('Purpose')
    keeperDate = keeper_attr('Date')
    keeperKeywords = keeper_attr('Keywords')
    keeperLineage = XMLLineage
    keeperHorizontalPosAccr = XMLHorizontalPosAccr
    keeperLinkage = XMLLinkage


    print 'Below is the information used to populate the XML:\n\
         Title:', keeperTitle,'\n\
         Abstract:', keeperAbs, '\n\
         Purpose:', keeperPurpose, '\n\
         Date:', keeperDate, '\n\
         Keywords:', keeperKeywords, '\n\
         Lineage:', keeperLineage, '\n\
         Linkage:', keeperLinkage, '\n\
         Horizontal Position Accuracy:', keeperHorizontalPosAccr, '\n'

    createXMLPrompt = raw_input('Press enter to create the XML or X to exit\n')

    if createXMLPrompt.lower == 'x':
        exit()


    outputXML = os.path.join(fullPath,"final_XMLs\\template.xml")

    tree = ET.parse(inputTemplatePath)
    root = tree.getroot()

    dataqual = ET.SubElement(root, 'dataqual')
    posacc = ET.SubElement(dataqual, 'posacc')
    horizpa = ET.SubElement(posacc, 'horizpa')
    horizpar = ET.SubElement(horizpa, 'horizpar')

    title = root.find('idinfo/citation/citeinfo/title')
    date = root.find('idinfo/citation/citeinfo/pubdate')
    #lineage = root.find('Esri/DataProperties/lineage/Process')
    keywords = root.find('idinfo/keywords/theme/themekey')
    linkage = root.find('idinfo/citation/citeinfo/onlink')
    abstract = root.find('idinfo/descript/abstract')

    #htmlKeeperAbs = '&lt;DIV STYLE="text-align:Left;"&gt;&lt;DIV&gt;&lt;DIV&gt;&lt;P&gt;&lt;SPAN&gt;'+keeperAbs+';/SPAN&gt;&lt;/P&gt;&lt;/DIV&gt;&lt;/DIV&gt;&lt;/DIV&gt;'
    title.text = keeperTitle
    date.text = keeperDate
    #lineage.text = keeperLineage
    keywords.text = keeperKeywords
    linkage.text = keeperLinkage
    abstract.text = keeperAbs
    horizpar.text = keeperHorizontalPosAccr

    tree.write(outputXML)

    status = import_XML()
    if status == 0:
        f = open(completeXML, 'a')
        f.write(record)
        f.write('\n')
        f.close()
        print 'Wrote to complete.'

    else:
        f = open(incompleteXML, 'a')
        f.write(record)
        f.write('\n')
        f.close()
        print 'Wrote to incomplete.'