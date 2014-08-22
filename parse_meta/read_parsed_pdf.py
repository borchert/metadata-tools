import os
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

userName = os.environ.get('USERNAME')

if os.path.exists(r'D:\drive\\'):
    drivePath = r'D:\drive\Map Library Projects\MGS'
elif os.path.exists(os.path.join(r'C:\Users\\',userName,'Google Drive')):
    drivePath = os.path.join(r'C:\Users\\',userName,'Google Drive\Map Library Projects\MGS')
else:
    drivePath = getDrivePath()

toDo = os.path.join(drivePath,'metaParsed.txt')
contentStrip = []

with open(toDo) as f:
    content = f.readlines()
    contentStrip = []
    holder = ''
    for x in content:
        if x.endswith('\n'):
            if x.startswith('\t'):
                holder = x[-1:].strip()
            else:
                holder = x[:-1].strip()
        else:
            holder = x
        contentStrip.append(holder)

for x in contentStrip:

    xSize = os.path.getsize(x)
    workingDir =x[:57]

    file_list = []

    os.chdir(workingDir)
    for file in glob.glob("*.txt"):
        fileSize = os.path.getsize(file)

        if fileSize == 0:
            print 'Skipped (zero size) -',file
        elif fileSize < xSize - 600:
            file_list.append(file)
        else:
            print 'Skipped (same size as non-parsed) -',file

    for x in file_list:
        read_file = os.path.join(workingDir,x)

        with open(read_file) as f:
            print '\n',read_file
            content = f.readlines()
            contentStrip = []
            holder = ''
            for x in content:
                if len(x)>2:
                    if x.endswith('\n'):
                        if x.startswith('\t'):
                            holder = x[-1:].strip()
                        else:
                            holder = x[:-1].strip()
                else:
                    holder = x
                contentStrip.append(holder)

        dataSet = 0
        holder = 0
        metaDict = {}

       # print file_list

        for i, x in enumerate(contentStrip):

            if 'bgpgp' in contentStrip[0]:
                #print 'Skipping this STUPID broken FILE\n'
                break

                # Maybe working?
            if 'Horizontal Positional Accuracy' in x:
                if len(contentStrip[i]) != 30:
                    hpa = x[31:]
                    metaDict['hpa'] = hpa
                    #print 'HPA = ',hpa

            # Maybe?
            if 'Purpose' in x:
                if contentStrip[i-2] in ['Abstract']:
                    purpose = contentStrip[i-1]
                else:
                    purpose = contentStrip[i-2]
                title = purpose
                if len(purpose) <= 5:
                    #print 'Purpose/title unavailable'
                    metaDict['purpose'] = 'Purpose and title unavailable'
                else:
                    #print 'Purpose = ', purpose
                    #print 'Title = ', title
                    metaDict['purpose'] = purpose
                    metaDict['title'] = purpose

            # Maybe?
            if 'Lineage' in x:
                if contentStrip[i-2] in ['Vertical Positional Accuracy']:
                    lineage = contentStrip[i-1]
                else:
                    lineage = contentStrip[i-2]
                if len(lineage) <= 5:
                    metaDict['lineage'] = 'Lineage unavailable'
                    #print 'Lineage unavailable'
                else:
                    #print 'Lineage = ', lineage
                    metaDict['lineage'] = lineage

            if 'Publication Date' in x:
                if len(contentStrip[i]) != 16:
                    pubDate = x[17:]
                    #print 'Publication Date = ', pubDate
                    metaDict['pubDate'] = pubDate

            if 'Time Period of Content' in x:
                if len(contentStrip[i]) != 22:
                    timePeriod = x[23:]
                    #print 'Time Period of Content = ', timePeriod

                elif contentStrip[i-1] in ('Purpose', 'Abstract'):
                    timePeriod= 'Time Period of Content not available'

                else:
                    timePeriod = contentStrip[i-2]
                    #print 'Time Period of Content = ', timePeriod
                metaDict['time'] = timePeriod

            if 'Publisher' in x:
                if len(contentStrip[i]) != 9:
                    publisher = x[10:]
                    #print 'Publisher = ', publisher
                else:
                    publisher = 'Publisher not available'
                metaDict['publisher'] = publisher

        f.close()

        metaDictTxt = os.path.join(read_file[:-4]+ '_metaDict.txt')
        f = open(metaDictTxt, 'w')
        f.write(str(metaDict))
        f.close()

