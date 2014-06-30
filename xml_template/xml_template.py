import time
import datetime

def processMeta(metaPath):
    with open(metaPath) as f:
        content = f.readlines()

    contentStrip = []
    holder = ''
    for x in content:
        if len(x)>2:
            if x.endswith('\n'):
                if x.startswith('\t'):
                    holder = x[-1:]
                else:
                    holder =  x[:-1]
        else:
            holder = x
        contentStrip.append(holder)

    findChar = ':'
    tagDict = {}
    for x in contentStrip:
        colon = x.find(findChar)
        if colon != -1:
            field = x[colon+2:]
            tag = x[:colon+1]
            tagDict[tag]=field

    f.close
    return tagDict

metaPath = r'c:/users/mart3565/desktop/test_meta.txt'
tagDict = processMeta(metaPath)

UTMZone = tagDict['Coordinate system:']
UTMPos = UTMZone.find('Zone')

# XML variables for *.docs

abstract = tagDict['Description of map:']
accessConstraint = 'Public'
attributeAccuracy = ''
contactAdd = ''
contactEmail = ''
contactOrg = tagDict['Publishing organization:']
contactVoice = ''
currentnessReference = ''
entityAndAttributeOverview = tagDict['GIS files associated with map from ArcInfo:']
horizontalPositionalAccuracy = tagDict['Horizontal accuracy (appropriate to final map scale):']
lineage = tagDict['Summary of procedures for compiling data used to make map:']
mapProjectionName = tagDict['Coordinate system:']
mapUnits = tagDict['Map units:']
metadataStandardName = 'None'
origin = tagDict['Publishing organization:']
publicationDate = tagDict['Date of publication:']
publisher= tagDict['Publishing organization:']
purpose = tagDict['Description of map:']

spatialExt = ''
timePeriodOfContent = tagDict['Date of data:']
title = tagDict['Map name:']
UTMzoneNumber = UTMZone[UTMPos:UTMPos+7]
verticalPositionalAccuracy = ''

eastBoundingCoordinate = ''
northBoundingCoordinate = ''
southBoundingCoordinate = ''
westBoundingCoordinate = ''

# date/time
today = datetime.date.today()
currenttime = str(time.strftime("%H:%M:%S"))
currentdate = today.strftime("%Y/%m/%d")

# Keyword parsing
keywords = tagDict['Map key words:']

pkeys = []
tkeys = []
keys = []

word = ''
position = 1

for char in keywords:
    if char !=',':
        word+=char
        if position == len(keywords):
            keys.append(word)
    else:
        keys.append(word)
        word = ''
    position +=1


for x in keys:
    for char in x:
        if char.isupper():
            pkeys.append(x)
            break
    else:
        tkeys.append(x)

placeKeywords = ''
themeKeywords = ''
counter = 1
for x in tkeys:
    if counter == len(tkeys):
        themeKeywords +=x
    else:
        themeKeywords+=x
        themeKeywords+=', '
    counter +=1

counter = 1

for x in pkeys:
    if counter == len(pkeys):
        placeKeywords+=x
    else:
        placeKeywords+=x
        placeKeywords+=', '
    counter+=1

# Source scale parsing

findChar = ':'
scale = tagDict['Map scale:']
colon = scale.find(findChar)
sourceScaleDenominator = scale[colon+1:]


# XML Template

createXML = '<metadata>\n\
<idinfo>\n\
<citation>\n\
<citeinfo>\n\
<origin>' + origin + '</origin>\n\
<pubdate>' + publicationDate + '</pubdate>\n\
<title>' + title + '</title>\n\
<mgmg1cid></mgmg1cid>\n\
<pubinfo>\n\
<publish>' + publisher + '</publish>\n\
</pubinfo>\n\
<onlink></onlink>\n\
</citeinfo>\n\
</citation>\n\
<descript>\n\
<abstract>' + abstract + '</abstract>\n\
<purpose>' + purpose + '</purpose>\n\
<supplinf>' + spatialExt + '</supplinf>\n\
</descript>\n\
<timeperd>\n\
<timeinfo>\n\
<sngdate>\n\
<caldate>' + timePeriodOfContent + '</caldate>\n\
</sngdate>\n\
</timeinfo>\n\
<current>' + currentnessReference + '</current>\n\
</timeperd>\n\
<status>\n\
<progress></progress>\n\
<update></update>\n\
</status>\n\
<spdom>\n\
<bounding>\n\
<westbc>' + westBoundingCoordinate + '</westbc>\n\
<eastbc>' + eastBoundingCoordinate + '</eastbc>\n\
<northbc>' + northBoundingCoordinate + '</northbc>\n\
<southbc>' + southBoundingCoordinate + '</southbc>\n\
</bounding>\n\
</spdom>\n\
<keywords>\n\
<theme>\n\
<themekt/>\n\
<themekey>' + themeKeywords + '</themekey>\n\
</theme>\n\
<place>\n\
<placekey>' + placeKeywords + '</placekey>\n\
</place>\n\
</keywords>\n\
<accconst>' + accessConstraint + '</accconst>\n\
<useconst></useconst>\n\
<ptcontac>\n\
<cntinfo>\n\
<cntperp>\n\
<cntper></cntper>\n\
<cntorg>' + contactOrg + '</cntorg>\n\
</cntperp>\n\
<cntpos></cntpos>\n\
<cntaddr>\n\
<addrtype>mailing and physical address</addrtype>\n\
<address>' + contactAdd + '</address>\n\
<city></city>\n\
<state></state>\n\
<postal></postal>\n\
</cntaddr>\n\
<cntvoice>' + contactVoice + '</cntvoice>\n\
<cntfax></cntfax>\n\
<cntemail>' + contactEmail + '</cntemail>\n\
</cntinfo>\n\
</ptcontac>\n\
<browse>\n\
<browsen>\n\
</browsen>\n\
<browsed></browsed>\n\
</browse>\n\
<native></native>\n\
<crossref>\n\
<citeinfo>\n\
<title>' + title + '</title>\n\
</citeinfo>\n\
</crossref>\n\
</idinfo>\n\
<dataqual>\n\
<attracc>\n\
<attraccr>' + attributeAccuracy + '</attraccr>\n\
</attracc>\n\
<logic></logic>\n\
<complete></complete>\n\
<posacc>\n\
<horizpa>\n\
<horizpar>' + horizontalPositionalAccuracy + '</horizpar>\n\
</horizpa>\n\
<vertacc>\n\
<vertaccr>' + verticalPositionalAccuracy + '</vertaccr>\n\
</vertacc>\n\
</posacc>\n\
<lineage>' + lineage + '\n\
<srcinfo>\n\
<srcscale>' + sourceScaleDenominator + '</srcscale>\n\
</srcinfo>\n\
<procstep>\n\
<procdesc></procdesc>\n\
</procstep>\n\
</lineage>\n\
</dataqual>\n\
<spdoinfo>\n\
<indspref></indspref>\n\
<direct></direct>\n\
<mgmg3obj></mgmg3obj>\n\
<mgmg3til></mgmg3til>\n\
</spdoinfo>\n\
<spref>\n\
<horizsys>\n\
<geograph>\n\
<latres/>\n\
<longres/>\n\
<geogunit/>\n\
</geograph>\n\
<planar>\n\
<mapproj>\n\
<mapprojn>' + mapProjectionName + '<mapprojn/>\n\
<mgmg4par/>\n\
<otherprj/>\n\
</mapproj>\n\
<gridsys>\n\
<gridsysn></gridsysn>\n\
<utm>\n\
<utmzone>' + UTMzoneNumber + '</utmzone>\n\
</utm>\n\
<spcs>\n\
<spcszone/>\n\
</spcs>\n\
<mgmg4coz/>\n\
<mgmg4adj/>\n\
</gridsys>\n\
<planci>\n\
<coordrep>\n\
<absres/>\n\
<ordres/>\n\
</coordrep>\n\
<distbrep>\n\
<distres></distres>\n\
</distbrep>\n\
<plandu>' + mapUnits + '</plandu>\n\
</planci>\n\
</planar>\n\
<geodetic>\n\
<horizdn></horizdn>\n\
<ellips></ellips>\n\
</geodetic>\n\
</horizsys>\n\
<vertdef>\n\
<altsys>\n\
<altdatum/>\n\
<altunits/>\n\
</altsys>\n\
<depthsys>\n\
<depthdn/>\n\
<depthdu/>\n\
</depthsys>\n\
</vertdef>\n\
</spref>\n\
<eainfo>\n\
<overview>\n\
<eaover>' + entityAndAttributeOverview + '</eaover>\n\
<eadetcit></eadetcit>\n\
</overview>\n\
</eainfo>\n\
<distinfo>\n\
<distrib>\n\
<cntinfo>\n\
<cntperp>\n\
<cntper></cntper>\n\
<cntorg>' + contactOrg + '</cntorg>\n\
</cntperp>\n\
<cntpos></cntpos>\n\
<cntaddr>\n\
<addrtype>mailing and physical address</addrtype>\n\
<address>' + contactAdd + '</address>\n\
<city></city>\n\
<state></state>\n\
<postal></postal>\n\
</cntaddr>\n\
<cntvoice>' + contactVoice + '</cntvoice>\n\
<cntfax></cntfax>\n\
<cntemail>' + contactEmail + '</cntemail>\n\
</cntinfo>\n\
</distrib>\n\
<resdesc></resdesc>\n\
<distliab></distliab>\n\
<stdorder>\n\
<digform>\n\
<digtinfo>\n\
<formname></formname>\n\
<formvern></formvern>\n\
<transize></transize>\n\
</digtinfo>\n\
</digform>\n\
<ordering></ordering>\n\
</stdorder>\n\
</distinfo>\n\
<metainfo>\n\
<metd></metd>\n\
<metc>\n\
<cntinfo>\n\
<cntperp>\n\
<cntper></cntper>\n\
<cntorg>' + contactOrg + '</cntorg>\n\
</cntperp>\n\
<cntpos></cntpos>\n\
<cntaddr>\n\
<addrtype>mailing and physical address</addrtype>\n\
<address>' + contactAdd + '</address>\n\
<city></city>\n\
<state></state>\n\
<postal></postal>\n\
</cntaddr>\n\
<cntvoice>' + contactVoice + '</cntvoice>\n\
<cntfax></cntfax>\n\
<cntemail>' + contactEmail + '</cntemail>\n\
</cntinfo>\n\
</metc>\n\
<metstdn>' + metadataStandardName + '</metstdn>\n\
<metstdv></metstdv>\n\
<metextns>\n\
<onlink></onlink>\n\
</metextns>\n\
</metainfo>\n\
<Esri>\n\
<ModDate>' + currentdate + '</ModDate>\n\
<ModTime>' + currenttime + '</ModTime>\n\
</Esri>\n\
<mdDateSt Sync="TRUE">' + currentdate + '</mdDateSt>\n\
</metadata>\n'

filePath = r'c:/users/mart3565/desktop/xmltest.xml'

file = open(filePath, 'w')
file.write(createXML)
file.close
