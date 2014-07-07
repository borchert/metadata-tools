import time
import datetime
import xml.etree.ElementTree as ET
import glob
import re
import os

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

def createDownloads(path):
    with open(path) as f:
        content = f.readlines()

    contentStrip = []
    idDownloaddict = {}

    for x in content:
        if x.endswith('\n'):
            contentStrip.append(x[:-1])
        else:
            contentStrip.append(x)

    findChar = ','
    for x in contentStrip:
        comma = x.find(findChar)
        link = x[comma+1:]
        id = x[:comma]
        idDownloaddict[id]=link

    f.close

    return idDownloaddict

""" FAILED"""
"""def convertDocToText(recordID):
    inPath = r'D:/drive/Map Library Projects/MGS/Records/' + recordID + '/temporary/'
    docLow = inPath + '*.doc'
    docUpp = inPath + '*.DOC'
    f = glob.glob(docLow) + glob.glob(docUpp)
    print inPath
    print docLow
    print docUpp

    outDir = inPath + 'txts'

    print outDir

    if not os.path.exists(outDir):
        os.makedirs(outDir)
    for i in f:
        print i
        os.system("catdoc -w '%s' > '%s'" %
              (i, outDir + '/' + re.sub(r".*/([^.]+)\.doc", r'\1.txt', i,
                                   flags=re.IGNORECASE)))"""

idDownloadPath = r'D:/drive/Map Library Projects/MGS/Scripts/XMLTemplate/ID_download_list.csv'
recordID = raw_input('Record ID: ')
temporaryDir = r'D:/drive/Map Library Projects/MGS/Records/' + recordID + '/temporary/'

for item in os.listdir(temporaryDir):
    #try:
    if item.endswith('.txt'):
        metaName = item[:-4]
        metaPath = r'D:/drive/Map Library Projects/MGS/Records/' + recordID + '/temporary/' + metaName + '.txt'
        outPath = r'D:/drive/Map Library Projects/MGS/Records/' + recordID + '/converted/' + metaName + '.xml'
        tagDict = processMeta(metaPath)
        print tagDict
        idDownloaddict = createDownloads(idDownloadPath)

        UTMZone = tagDict['Coordinate system:']
        UTMPos = UTMZone.find('Zone')

        failedTags = []

        # XML variables for *.docs

        try:
            abstractT = tagDict['Description of map:']
        except:
            abstractT = ''
            failedTags.append('abstractT')

        accessConstraintT = 'Public'
        attributeAccuracyT = ''
        contactAddT = 'GIS Staff, Minnesota Geological Survey, University of Minnesota'
        contactEmailT = 'mgsgis@umn.edu'

        try:
            contactOrgT = tagDict['Publishing organization:']
        except:
            contactOrgT = ''
            failedTags.append('contactOrgT')

        contactVoiceT = '612-627-4780'
        currentnessReferenceT = ''

        try:
            downloadLinkT = idDownloaddict[recordID]
        except:
            downloadLinkT = ''
            failedTags.append('downloadLinkT')

        try:
            entityAndAttributeOverviewT = tagDict['GIS files associated with map from ArcInfo:']
        except:
            entityAndAttributeOverviewT = ''
            failedTags.append('entityAndAttributeOverviewT')

        try:
            horizontalPositionalAccuracyT = tagDict['Horizontal accuracy (appropriate to final map scale):']
        except:
            horizontalPositionalAccuracyT = ''
            failedTags.append('horizontalPositionalAccuracyT')

        try:
            lineageT = tagDict['Summary of procedures for compiling data used to make map:']
        except:
            lineageT = ''
            failedTags.append('lineageT')

        try:
            mapProjectionNameT = tagDict['Coordinate system:']
        except:
            mapProjectionNameT = ''
            failedTags.append('mapProjectionNameT')

        try:
            mapUnitsT = tagDict['Map units:']
        except:
            mapUnitsT = ''
            failedTags.append('mapUnitsT')

        metadataStandardNameT = 'None'

        try:
            originT = tagDict['Publishing organization:']
        except:
            originT = ''
            failedTags.append('originT')

        try:
            publicationDateT = tagDict['Date of publication:']
        except:
            publicationDateT = ''
            failedTags.append('publicationDateT')

        try:
            publisherT = tagDict['Publishing organization:']
        except:
            publisherT = ''
            failedTags.append('publisherT')

        try:
            purposeT = tagDict['Description of map:']
        except:
            purposeT = ''
            failedTags.append('purposeT')

        spatialExtT = ''

        try:
            timePeriodOfContentT = tagDict['Date of data:']
        except:
            timePeriodOfContentT = ''
            failedTags.append('timePeriodOfContentT')

        try:
            titleT = tagDict['Map name:']
        except:
            titleT = ''
            failedTags.append('titleT')

        try:
            UTMzoneNumberT = UTMZone[UTMPos:UTMPos+7]
        except:
            UTMzoneNumberT = ''
            failedTags.append('UTMzoneNumberT')

        verticalPositionalAccuracyT = ''

        eastBoundingCoordinateT = ''
        northBoundingCoordinateT = ''
        southBoundingCoordinateT = ''
        westBoundingCoordinateT = ''

        # date/time
        today = datetime.date.today()
        currenttimeT = str(time.strftime("%H:%M:%S"))
        currentdateT = today.strftime("%Y/%m/%d")

        # Keyword parsing
        keywordsT = tagDict['Map key words:']

        pkeys = []
        tkeys = []
        keys = []

        word = ''
        position = 1

        for char in keywordsT:
            if char !=',':
                word+=char
                if position == len(keywordsT):
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
        sourceScaleDenominatorT = scale[colon+1:]


        # XML Template

        ''' build element tree '''

        root = ET.Element('metadata')
        idinfo = ET.SubElement(root, 'idinfo')
        citation = ET.SubElement(idinfo, 'citation')
        citeinfo = ET.SubElement(citation, 'citeinfo')

        origin = ET.SubElement(citeinfo, 'origin')
        origin.text = originT

        pubdate = ET.SubElement(citeinfo, 'pubdate')
        pubdate.text = publicationDateT

        title = ET.SubElement(citeinfo, 'title')
        title.text = titleT

        mgmglcid = ET.SubElement(citeinfo, 'mgmglcid')
        pubinfo = ET.SubElement(citeinfo, 'pubinfo')

        publish = ET.SubElement(pubinfo, 'publish')
        publish.text = publisherT

        onlink = ET.SubElement(citeinfo, 'onlink')
        onlink.text = downloadLinkT

        descript = ET.SubElement(idinfo, 'descript')

        abstract = ET.SubElement(descript, 'abstract')
        abstract.text = abstractT

        purpose = ET.SubElement(descript, 'purpose')
        purpose.text = purposeT

        supplinf = ET.SubElement(descript, 'supplinf')
        supplinf.text = spatialExtT

        timeperd = ET.SubElement(idinfo, 'timeperd')
        timeinfo = ET.SubElement(timeperd, 'timeinfo')
        sngdate = ET.SubElement(timeinfo, 'sngdate')

        caldate = ET.SubElement(sngdate, 'caldate')
        caldate.text = timePeriodOfContentT

        current = ET.SubElement(timeperd, 'current')
        current.text = currentnessReferenceT

        status = ET.SubElement(idinfo, 'status')
        progress = ET.SubElement(status, 'progress')
        update = ET.SubElement(status, 'update')
        spdom = ET.SubElement(idinfo, 'spdom')
        bounding = ET.SubElement(spdom, 'bounding')

        westbc = ET.SubElement(bounding, 'westbc')
        westbc.text = westBoundingCoordinateT

        eastbc = ET.SubElement(bounding, 'eastbc')
        eastbc.text = eastBoundingCoordinateT

        northbc = ET.SubElement(bounding, 'northbc')
        northbc.text = northBoundingCoordinateT

        southbc = ET.SubElement(bounding, 'south')
        southbc.text = southBoundingCoordinateT

        keywords = ET.SubElement(idinfo, 'keywords')
        theme = ET.SubElement(keywords, 'theme')
        themekt = ET.SubElement(theme, 'themekt')

        themekey = ET.SubElement(theme, 'themekey')
        themekey.text = themeKeywords

        place = ET.SubElement(keywords, 'place')

        placekey = ET.SubElement(place, 'placekey')
        placekey.text = placeKeywords

        accconst = ET.SubElement(idinfo, 'accconst')
        accconst.text = accessConstraintT

        useconst = ET.SubElement(idinfo, 'useconst')
        ptcontac = ET.SubElement(idinfo, 'ptcontac')
        cntinfo = ET.SubElement(ptcontac, 'cntinfo')
        cntperp = ET.SubElement(cntinfo, 'cntperp')
        cntper = ET.SubElement(cntperp, 'cntper')

        cntorg = ET.SubElement(cntperp, 'cntorg')
        cntorg.text = contactOrgT

        cntpos = ET.SubElement(cntinfo, 'cntpos')
        cntaddr = ET.SubElement(cntinfo, 'cntaddr')

        addrtype = ET.SubElement(cntaddr, 'addrtype')
        addrtype.text = 'mailing and physical address'

        address = ET.SubElement(cntaddr, 'address')
        address.text = contactAddT

        city = ET.SubElement(cntaddr, 'city')
        state = ET.SubElement(cntaddr, 'state')
        postal = ET.SubElement(cntaddr, 'postal')

        cntvoice = ET.SubElement(cntinfo, 'cntvoice')
        cntvoice.text = contactVoiceT

        cntfax = ET.SubElement(cntinfo, 'cntfax')

        cntemail = ET.SubElement(cntaddr, 'cntemail')
        cntemail.text = contactEmailT

        browse = ET.SubElement(idinfo, 'browse')
        browsen = ET.SubElement(browse, 'browsen')
        browsed = ET.SubElement(browse, 'browsed')
        native = ET.SubElement(idinfo, 'native')
        crossref = ET.SubElement(idinfo, 'crossref')
        citeinfo = ET.SubElement(crossref, 'citeinfo')

        title = ET.SubElement(crossref, 'title')
        title.text = titleT

        dataqual = ET.SubElement(root, 'dataqual')
        attracc = ET.SubElement(dataqual, 'attracc')

        attraccr = ET.SubElement(attracc, 'attraccr')
        attraccr.text = attributeAccuracyT

        logic = ET.SubElement(dataqual, 'logic')
        complete = ET.SubElement(dataqual, 'complete')
        posacc = ET.SubElement(dataqual, 'posacc')
        horizpa = ET.SubElement(posacc, 'horizpa')

        horizpar = ET.SubElement(horizpa, 'horizpar')
        horizpar.text = horizontalPositionalAccuracyT

        vertacc = ET.SubElement(posacc, 'vertacc')

        vertaccr = ET.SubElement(vertacc, 'vertaccr')
        vertaccr.text = verticalPositionalAccuracyT

        lineage = ET.SubElement(dataqual, 'lineage')
        lineage.text = lineageT

        srcinfo = ET.SubElement(lineage, 'srcinfo')

        srcscale = ET.SubElement(srcinfo, 'srcscale')
        srcscale.text = sourceScaleDenominatorT

        procstep = ET.SubElement(lineage, 'procstep')
        procdesc = ET.SubElement(procstep, 'procdesc')
        spdoinfo = ET.SubElement(root, 'spdoinfo')
        indspref = ET.SubElement(spdoinfo, 'indspref')
        direct = ET.SubElement(spdoinfo, 'direct')
        mgmg3obj = ET.SubElement(spdoinfo, 'mgmg3obj')
        mgmg3til = ET.SubElement(spdoinfo, 'mgmg3til')
        spref = ET.SubElement(root, 'spref')
        horizsys = ET.SubElement(spref, 'horizsys')
        geograph = ET.SubElement(horizsys, 'geograph')
        latres = ET.SubElement(geograph, 'latres')
        longres = ET.SubElement(geograph, 'longres')
        geogunit = ET.SubElement(geograph, 'geogunit')
        planar = ET.SubElement(horizsys, 'planar')
        mapproj = ET.SubElement(planar, 'mapproj')

        mapprojn = ET.SubElement(mapproj, 'mapprojn')
        mapprojn.text = mapProjectionNameT

        mgmg4par = ET.SubElement(mapproj, 'mgmg4par')
        otherprj = ET.SubElement(mapproj, 'otherprj')
        gridsys = ET.SubElement(planar, 'gridsys')
        gridsysn = ET.SubElement(gridsys, 'gridsysn')
        utm = ET.SubElement(gridsys, 'utm')

        utmzone = ET.SubElement(utm, 'utmzone')
        utmzone.text = UTMzoneNumberT

        spcs = ET.SubElement(gridsys, 'spcs')
        spcszone = ET.SubElement(spcs, 'spcszone')
        mgmg4coz = ET.SubElement(gridsys, 'mgmg4coz')
        mgmg4adj = ET.SubElement(gridsys, 'mgmg4adj')
        planci = ET.SubElement(planar, 'planci')
        coordrep = ET.SubElement(planci, 'coordrep')
        absres = ET.SubElement(coordrep, 'absres')
        ordres = ET.SubElement(coordrep, 'ordres')
        distbrep = ET.SubElement(planci, 'distbrep')
        distres = ET.SubElement(distbrep, 'distres')

        plandu = ET.SubElement(planci, 'plandu')
        plandu.text = mapUnitsT

        geodetic = ET.SubElement(horizsys, 'geodetic')
        horizdn = ET.SubElement(geodetic, 'horizdn')
        ellips = ET.SubElement(geodetic, 'ellips')
        vertdef = ET.SubElement(spref, 'vertdef')
        altsys = ET.SubElement(vertdef, 'altsys')
        altdatum = ET.SubElement(altsys, 'altdatum')
        altunits = ET.SubElement(altsys, 'altunits')
        depthsys = ET.SubElement(vertdef, 'depthsys')
        depthdn = ET.SubElement(depthsys, 'depthdn')
        depthdu = ET.SubElement(depthsys, 'depthdu')
        eainfo = ET.SubElement(root, 'eainfo')
        overview = ET.SubElement(eainfo, 'overview')

        eaover = ET.SubElement(overview, 'eaover')
        eaover.text = entityAndAttributeOverviewT

        eadetcit = ET.SubElement(overview, 'eadetcit')
        distinfo = ET.SubElement(root, 'distinfo')
        distrib = ET.SubElement(distinfo, 'distrub')
        cntinfo = ET.SubElement(distrib, 'cntinfo')
        cntperp = ET.SubElement(distrib, 'cntperp1')
        cntper = ET.SubElement(cntperp, 'cntper')

        cntorg = ET.SubElement(cntperp, 'cntorg')
        cntorg.text = contactOrgT

        cntpos = ET.SubElement(cntinfo, 'cntpos')
        cntaddr = ET.SubElement(cntinfo, 'cntaddr')

        addrtype = ET.SubElement(cntaddr, 'addrtype')
        addrtype.text = 'mailing and physical address'

        address = ET.SubElement(cntaddr, 'address')
        address.text = contactAddT

        city = ET.SubElement(cntaddr, 'city')
        state = ET.SubElement(cntaddr, 'state')
        postal = ET.SubElement(cntaddr, 'postal')

        cntvoice = ET.SubElement(cntinfo, 'cntvoice')
        cntvoice.text = contactVoiceT

        cntfax = ET.SubElement(cntinfo, 'cntfax')

        cntemail = ET.SubElement(cntinfo, 'cntemail')
        cntemail.text = contactEmailT

        resdesc = ET.SubElement(distinfo, 'resdesc')
        distliab = ET.SubElement(distinfo, 'distliab')
        stdorder = ET.SubElement(distinfo, 'stdorder')
        digform = ET.SubElement(stdorder, 'digform')
        digtinfo = ET.SubElement(digform, 'digtinfo')
        formname = ET.SubElement(digtinfo, 'formname')
        formvern = ET.SubElement(digtinfo, 'formvern')
        transize = ET.SubElement(digtinfo, 'transize')
        ordering = ET.SubElement(stdorder, 'ordering')
        metainfo = ET.SubElement(root, 'metainfo')
        metd = ET.SubElement(metainfo, 'metd')
        metc = ET.SubElement(metainfo, 'metc')
        cntinfo = ET.SubElement(metc, 'cntinfo')
        cntperp = ET.SubElement(metc, 'cntperp')
        cntper = ET.SubElement(cntperp, 'cntper')

        cntorg = ET.SubElement(cntperp, 'cntorg')
        cntorg.text = contactOrgT

        cntpos = ET.SubElement(cntinfo, 'cntpos')
        cntaddr = ET.SubElement(cntinfo, 'cntaddr')

        addrtype = ET.SubElement(cntaddr, 'addrtype')
        addrtype.text = 'mailing and physical address'

        address = ET.SubElement(cntaddr, 'address')
        address.text = contactAddT

        city = ET.SubElement(cntaddr, 'city')
        state = ET.SubElement(cntaddr, 'state')
        postal = ET.SubElement(cntaddr, 'postal')

        cntvoice = ET.SubElement(cntinfo, 'cntvoice')
        cntvoice.text = contactVoiceT

        cntfax = ET.SubElement(cntinfo, 'cntfax')

        cntemail = ET.SubElement(cntinfo, 'cntemail')
        cntemail.text = contactEmailT

        metstdn = ET.SubElement(metainfo, 'metstdn')
        metstdn.text = metadataStandardNameT

        metstdv = ET.SubElement(metainfo, 'metstdv')
        metextns = ET.SubElement(metainfo, 'metextns')

        onlink = ET.SubElement(metextns, 'onlink')
        onlink.text = downloadLinkT

        esri = ET.SubElement(root, 'Esri')

        moddate = ET.SubElement(esri, 'ModDate')
        moddate.text = currentdateT

        modtime = ET.SubElement(esri, 'ModTime')
        modtime.text = currenttimeT

        mdDateSt = ET.SubElement(root, 'mdDateSt')
        mdDateSt.text = currentdateT
        mdDateSt.set('Sync', 'TRUE')

        ''' Write tree '''
        tree = ET.ElementTree(root)
        tree.write(outPath)

        ''' Write failed tags '''
        failedTagsFile = r'D:/drive/Map Library Projects/MGS/Records/' + recordID + '/converted/' + metaName + '_failedtags.txt'
        f = open(failedTagsFile, 'w')
        for x in failedTags:
            f.write(x)
        f.close()


    """except:
        errorLog = failedTagsFile = r'D:/drive/Map Library Projects/MGS/Records/' + recordID + '/converted/' + recordID + '_errorlog.txt'
        print item + ' FAILED'
        e = open(errorLog, 'a')
        failMSG = item + ' - FAILED\n\n'
        e.write(failMSG)
        e.close"""
