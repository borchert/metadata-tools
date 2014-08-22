import subprocess
import os

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


failedTags = drivePath + r'\Documentation\failedtagscleanup.txt'

f = open(failedTags, 'r')
content = f.readlines()
filesToOpen = []
for x in content:
    holder = x[:-1]
    filesToOpen.append(holder)

count = 0
total = 0
for x in filesToOpen:
    path = x[:68] +'temporary/'
    if os.path.exists(path):
        pass
    else:
        path = x[:67] +'temporary/'
        if os.path.exists(path):
            pass
        else:
            path = x[:66] +'temporary/'
            if os.path.exists(path):
                pass
            else:
                path = x[:65] +'temporary/'

    f = x[len(path):]+'.txt'
    builtPath = path + f
    xmlPath = x + '.xml'
    if count < 5:
        print 'Opening:', builtPath
        subprocess.Popen([r'C:\Program Files (x86)\Notepad++\notepad++.exe', builtPath])
        subprocess.Popen([r'C:\Program Files (x86)\Notepad++\notepad++.exe', xmlPath])
        count+=1

    else:
        print 'Opening:', builtPath
        subprocess.Popen([r'C:\Program Files (x86)\Notepad++\notepad++.exe', builtPath])
        subprocess.Popen([r'C:\Program Files (x86)\Notepad++\notepad++.exe', xmlPath])
        count=0
        raw_input()
    total +=1
    print 'Completed :',total,'out of',len(filesToOpen),'records.'