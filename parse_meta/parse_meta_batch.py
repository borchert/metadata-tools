import os
import re

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

toDo = os.path.join(drivePath,'parse_meta_toDo.txt')

with open(toDo) as f:
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

listToDo = []
for x in contentStrip:
    fullPath = os.path.join(drivePath,x[25:]+'.txt')

    if os.path.isfile(fullPath):
        listToDo.append(fullPath)
    else:
        print 'MISSING - ', fullPath


total = 0
doneList = []
failedList = []

for x in listToDo:
    workingFile = x
    fullPath = x[:len(drivePath)+24]
    print '\nWorking on:',x
    text = open(x)
    read_text = text.read()
    search = [m.start() for m in re.finditer('Data Set Name', read_text)]

    find_sets = []
    print search

    for x in search:
        data_set = read_text[x+15:x+20]
        if len(data_set) != 0:
            if data_set not in find_sets:
                find_sets.append(data_set)

    find_sets_stripped =[]

    for x in find_sets:
        holder = ''
        if x.endswith('\n'):
            if x.startswith('\t'):
                holder = x[-1:].strip()
            else:
                holder = x[:-1].strip()
        else:
            holder = x
        contentStrip.append(holder)
        holder = x.strip()
        if holder.isalnum():
            find_sets_stripped.append(holder)

    master_list = []

    for x in find_sets_stripped:

        search_set = [m.start() for m in re.finditer(find_sets_stripped[find_sets_stripped.index(x)], read_text)]
        for i in search_set:
            if search_set[0] not in master_list:
                master_list.append(search_set[0])

    item = 0

    if len(master_list) != 0:
        for x in master_list:
            file_name= read_text[master_list[item]:master_list[item]+5].strip()
            print 'file name =', file_name
            outDir = fullPath[:58]
            print outDir
            text_file = os.path.join(outDir,file_name+'.txt')

            print 'text file =', text_file

            f=open(text_file,'w')

            print 'Opening text file'
            if item == len(master_list)-1:
                stuff = read_text[master_list[item]:]
            else:
                stuff = read_text[master_list[item]:master_list[item+1]]
            f.write(stuff)
            print 'Writing text file'
            item+=1
            print 'Completed'
            total +=1

            if workingFile not in doneList:
                doneList.append(workingFile)

    else:
        if workingFile not in failedList:
            failedList.append(workingFile)
        print 'No items found'


print doneList
print 'Total Completed: ', total

foundMeta = os.path.join(drivePath,'metaParsed.txt')
f = open(foundMeta,'a')
for x in doneList:
    f.write(x)
    f.write('\n')
f.close

noMeta = os.path.join(drivePath,'noMetaToParse.txt')
f = open(noMeta,'a')
for x in failedList:
    f.write(x)
    f.write('\n')
f.close()