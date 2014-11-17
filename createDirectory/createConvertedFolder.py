#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------
# createConvertedFolder.py
# Created on: 2014-07-07 
# Description: Creates a folder in every directory 1 level deep
# ---------------------------------------------------------------------------

# This script will create a directory (set up for /converted) in every
# directory found, limited to one level deep.

import os

startDir = os.getcwd()
startDepth = startDir.count(os.sep)
newDir = r'/converted'

print 'Beginning search.'

for root, dirs ,files in os.walk(startDir):
 
    #if beyond one level, don't do anything with files, and delete dir references
    #to avoid recursing further
    if root.count(os.sep) - startDepth > 1:
        del dirs[:]
    elif root.count(os.sep) - startDepth == 0:
        pass
    else:
        makeDir = root + newDir
        
        if not os.path.exists(makeDir):
            os.makedirs(makeDir)
            print 'Created: ' + str(makeDir)

        else:
            print root + '   --  Exists and skipped'
