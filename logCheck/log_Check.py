#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------
# log_Check.py
# Created on: 2014-06-13
# Description: Checks log creation status
# ---------------------------------------------------------------------------

# This script checks for the presence of various log files.

from __future__ import division
import os
import timeit

#folder hierarchy
path = 'C:\Users\mart3565\Desktop\done'
#path=os.getcwd()



def fold(path, output=None):
    #cwd = os.getcwd()

    logStatus = r'c:\Users\mart3565\desktop\python\logStatus.txt'
    file=open(logStatus, 'w')
    metadataLog = 'metadata_log.txt'
    fileDesc = 'file_desc.txt'
    fileStruct = 'fileStruct.txt'
    foldStruct = 'foldStruct.txt'
    #nl = '\n'*2
    meta = 0
    filed = 0
    fs = 0
    folds = 0
    status = []
    dirDepth = 0
    countflag = 0
    for root, dirs, files in os.walk(path):

        for name in files:

            if name == metadataLog:
                meta = 1
                #print 'meta', meta

            elif name == fileDesc:
                filed = 1
                #print 'FileD', filed


            elif name == fileStruct:
                fs = 1
                #print 'FileS', fs


            elif name == foldStruct:
                folds = 1
                #print 'FoldS', folds

            elif all(x == 1 for x in (meta,filed,fs,folds)):
                status.append('All accounted for!')
                break


        if meta != 1:
            status.append('No metadata')

        if filed != 1:
            status.append('No file description')

        if fs != 1:
            status.append('No file structure')

        if folds != 1:
            status.append('No folder structure')

        if len(status) == 0:
            if all(x == 1 for x in (meta,filed,fs,folds)):
                status.append('All accounted for!')

        directory = str(os.path.join(root))
        #print directory

        for x in status:
            print "Status", x
            #print x

        if path != directory:
            #print directory
            if status[0] != 'All accounted for!':

                print directory
                for x in status:
                    print x
                """elif:
                    for x in status:
                        print directory
                        print status[x]"""
            else:
                if countflag == 0:
                    print 'All Good'
                    countflag = 1


        """if dirDepth!=0:
            for x in status:

                pathName = str(os.path.join(root, path))
                if status[0] == 'All accounted for!':
                    pass
                else:
                    file.write(pathName)
                    pathDepth+=1
                file.write(x)"""

        #dirDepth+=1
        #print dirDepth
        status = []

        print 'status reset'

    file.close()

fold(path)
print 'Complete'
raw_input()
