#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------
# findFailedTagsFiles.py
# Created on: 2014-08-15
# Description: Opens failed tags with subprocess/Notepad++.
# ---------------------------------------------------------------------------

# This script open all files missing ALL tags in batches of 5, using subprocess
# and Notepad++.  Notepad++ must be present and the path may need to be altered.
# This is a subset of findFailedTagsFiles.py.

import find_Drive
import subprocess
import os

userName = os.environ.get('USERNAME')

drivePath = find_Drive.main()
notepadPath = r'C:\Program Files (x86)\Notepad++\notepad++.exe'

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
        subprocess.Popen([notepadPath, builtPath])
        subprocess.Popen([notepadPath, xmlPath])
        count+=1

    else:
        print 'Opening:', builtPath
        subprocess.Popen([notepadPath, builtPath])
        subprocess.Popen([notepadPath, xmlPath])
        count=0
        raw_input()
    total +=1
    print 'Completed :',total,'out of',len(filesToOpen),'records.'