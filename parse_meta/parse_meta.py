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

record = raw_input("Enter record number: ")
meta_path = raw_input("Enter metadata to parse: ")

f = os.path.join(drivePath,'Records',record,'temporary',meta_path+'.txt')
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

for x in master_list:
    file_name= read_text[master_list[item]:master_list[item]+5]
    text_file = os.path.join(drivePath,'Records',record,'temporary',file_name+'.txt')
    f=open(text_file,'w')
    if item == 13:
        stuff =read_text[master_list[item]:]
    else:
        stuff =read_text[master_list[item]:master_list[item+1]]
    f.write(stuff)
    item+=1