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

test = r'c:/users/mart3565/desktop/test.txt'
toDo = []
f = open(test)
content = f.readlines()
count = 0
for x in content:
    if count == len(content)-1:
        item = x[25:]
    else:
        item = x[25:-1]
    toDo.append(item)
    count+=1

listToDo = []
for x in toDo:
    fullPath = os.path.join(drivePath, x+'.txt')
    if os.path.isfile(fullPath):
        #print 'FOUND - ',fullPath
        listToDo.append(fullPath)
    else:
        print 'MISSING - ', fullPath


total = 0

for x in listToDo:
    f = x
    text = open(f)
    read_text = text.read()
    search = [m.start() for m in re.finditer('Data Set Name', read_text)]

    find_sets = []

    '''test_list = []
    test = ['bgnta','bgpga','bgpgp','dhpt','dkln','foln','hyln','lkpg','paan','papg','plsln','rdln1','rdln2','rdpt']

    for x in test:
        upper = x.upper()
        test_list.append(x)
        test_list.append(upper)'''

    for x in search:
        data_set =  read_text[x+15:x+20]
        if data_set not in find_sets:
            find_sets.append(data_set)

    find_sets_stripped =[]

    for x in find_sets:
        holder = x.strip(' ')
        if holder.isalnum():
            find_sets_stripped.append(holder)

    master_list = []

    for x in find_sets_stripped:

        #if x in test_list:
        search_set = [m.start() for m in re.finditer(find_sets_stripped[find_sets_stripped.index(x)], read_text)]
        #print x, '-', search_set, 'len:', len(search_set)
        for i in search_set:
            if search_set[0] not in master_list:
                master_list.append(search_set[0])

    item = 0


    #print master_list
    if len(master_list) != 0:
        for x in master_list:

            file_name= read_text[master_list[item]:master_list[item]+5]
            print 'file name =', file_name
            outDir = fullPath[:58]
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
    else:
        print 'No items found'

print 'Total Completed: ', total
