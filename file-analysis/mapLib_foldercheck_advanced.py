#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------
# mapLib_foldercheck_advanced.py
# Created on: 2014-06-27
# Description: Returns contents of directories as several text files.
# ---------------------------------------------------------------------------

# This script reports on he content of a directory in the form of four text files:

# 1) file_desc.txt
#    - file statistics (size, extension, etc.)
# 2) fileStruct.txt
#    - file structure as a tree (output or print)
# 3) foldStruct.txt
#    - folder structure as a tree (output or print)
# 4) metadata_log.txt
#    - potential metadata files (output or print)

from __future__ import division
import os
import timeit

def fold(path, output=None):
    writePath = str(path)+'\\foldStruct.txt'
    file=open(writePath, 'w')
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        if output == 'y':
            file.write('{}{}/'.format(indent, os.path.basename(root)) + '\n')
        else:
            print('{}{}/'.format(indent, os.path.basename(root)))
    file.close()

def foldFiles(path, output=None):
    writePath = str(path)+'\\fileStruct.txt'
    file=open(writePath, 'w')
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        #print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        file.write('{}{}/'.format(indent, os.path.basename(root)) + '\n')
        for f in files:
            if output == 'y':

                file.write('{}{}'.format(subindent, f) + '\n')
            else:
                print('{}{}'.format(subindent, f))
    file.close()

def humanize_bytes(bytes, precision=1):
    """Return a humanized string representation of a number of bytes.
    Assumes `from __future__ import division`.

    >>> humanize_bytes(1)
    '1 byte'
    >>> humanize_bytes(1024)
    '1.0 kB'
    >>> humanize_bytes(1024*123)
    '123.0 kB'
    >>> humanize_bytes(1024*12342)
    '12.1 MB'
    >>> humanize_bytes(1024*12342,2)
    '12.05 MB'
    >>> humanize_bytes(1024*1234,2)
    '1.21 MB'
    >>> humanize_bytes(1024*1234*1111,2)
    '1.31 GB'
    >>> humanize_bytes(1024*1234*1111,1)
    '1.3 GB'
    """
    abbrevs = (
        (1<<50L, 'PB'),
        (1<<40L, 'TB'),
        (1<<30L, 'GB'),
        (1<<20L, 'MB'),
        (1<<10L, 'kB'),
        (1, 'bytes')
    )
    if bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)

def sizeQuery(d):
    totalSize=0
    for v in d:
        value = d[v]
        valueSplit = value.split(None,1)
        totalSize += float(valueSplit[0])

    maxFileSize= max(d.values())
    for k,v in d.items():
        if v == maxFileSize:
            maxFile = k
    return (totalSize, maxFileSize, maxFile)

def metadataQuery(path, fileTypes, output=None):
    metadata=[]
    metadataTypes = {
                        '.pdf':0,
                        '.xml':0,
                        '.htm':0,
                        '.html':0,
                        '.doc':0,
                        '.docx':0,
                        '.txt':0
    }
    metadataSize={}
    likelyMetadata=[]

    for root, dirs, files in os.walk(path):

        for f in fileTypes:
            fileCount=0
            for name in files:
                #  Counts file if extension matches one found in fileTypes
                nameLow=name.lower()
                if any(nameLow.endswith(x) for x in (metadataTypes)):
                    if nameLow not in metadata:
                        if nameLow not in ['filestruct.txt', 'foldstruct.txt', 'metadata_log.txt', 'file_desc.txt']:
                            namePath = os.path.abspath(os.path.join(root, nameLow))
                            size = os.path.getsize(namePath)
                            sizeBytes = humanize_bytes(size)
                            metadata.append(nameLow)
                            metadataSize.update({nameLow:sizeBytes})
                            if 'metadata' in nameLow:
                                likelyMetadata.append(nameLow)
                            elif 'meta' in nameLow:
                                likelyMetadata.append(nameLow)


    for f in metadata:
        for x in metadataTypes:
            if f.endswith(x):
                metadataTypes[x]+=1

    totalSize, maxFileSize, maxFile = sizeQuery(metadataSize)


    if output == 'y':
        
        # WRITE TO FILE
        indent = ' ' * 4
        count = 0
        writePath = str(path)+'\\metadata_log.txt'
        file=open(writePath, 'w')
        file.write('Folder contains the following metadata file types and count: \n')
        for key, value in sorted(metadataTypes.items()):
            if value >0:
                if len(key)==4:
                    if count == 0:
                        keyval = indent + str(key)+ ' : '+ str(value)
                        count = 1
                    else:
                        keyval = ',' + indent + str(key)+ ' : '+ str(value)
                    #count+=1
                    #keyval = indent + str(key)+ ' : '+ str(value) + ','

                    file.write(keyval)
                else:
                    if count == 0:
                        keyval = indent + str(key)+ ': '+ str(value)
                    else:
                        keyval = ',' + indent + str(key)+ ': '+ str(value)
                    count+=1
                    #keyval = indent + str(key)+ ': '+ str(value)+ ','

                    file.write(keyval)
        file.write("\n\nThe following may be metadata files: \n")

        count = 0
        
        for x in sorted(metadata):
            if count == 0:
                file.write(indent + x)
                count=1
            else:
                file.write(',' + indent + x)


        count = 0

        
        if len(likelyMetadata) == 0:
            pass
        else:
            file.write("\n\nThe following are likely metadata files: \n")
            for x in sorted(likelyMetadata):
                if count == 0:
                    file.write(indent + x)
                    count=1
                else:
                    file.write(',' + indent + x)


        file.write('\n\nTotal metadata files: ' + str(len(metadata))+ '\n')
        #file.write('\nTotal metadata file size: '+'{:,}'.format(totalSize)+'kB'+ '\n')
        #file.write('\nLargest file: '+maxFile+ ' - '+ maxFileSize+ '\n')
        file.close()
        
    else:

        print 'Folder contains the following metadata file types and count: '
        for key, value in sorted(metadataTypes.items()):
            if len(key)==4:
                print key, ' : ', value
            else:
                print key, ': ', value

        print "\nThe following may be metadata files: "
        print sorted(metadata)

        print '\nTotal metadata files: ',str(len(metadata))
        #print metadataSize
        print '\nTotal metadata file size :','{:,}'.format(totalSize), 'kB'
        print '\nLargest file: ',maxFile, '-', maxFileSize

def countFilesasDict(path, output=None):

    fileTypes ={}
    failedTypes={}
    extCount=0
    fileCountTotal=0
    failedTypesCount=0
    fileCount = 0
    
    for root, dirs, files in os.walk(path):
        for name in files:

            extension = os.path.splitext(name)[1]
            extLow=extension.lower()
            if extLow in fileTypes:
                pass

            # Catch files with no extension (log, gdb) and adds to list failedTypes
            elif '.' not in name:
                if name not in failedTypes:
                    failedTypes.update({name:fileCount})

            # Add extension to list fileTypes
            else:
                if extLow not in ['.py']:
                    fileTypes.update({extLow:fileCount})
                    extCount+=1

    for root, dirs, files in os.walk(path):

        for f in fileTypes:
            fileCount=0
            for name in files:

                #  Counts file if extension matches one found in fileTypes
                nameLow=name.lower()

                if nameLow.endswith(f):
                    if nameLow not in ['filestruct.txt', 'foldstruct.txt', 'metadata_log.txt', 'file_desc.txt']:
                        if nameLow.endswith('.py'):
                            pass
                        else:
                            fileTypes[f]+=1
                            fileCount+=1

            fileCountTotal+=fileCount


        for f in failedTypes:
            fileCount=0
            for name in files:

                #  Counts files with no extension by matching to failedTypes list
                if name == f:
                    fileCount+=1
                    failedTypes[f]+=1
            fileCountTotal+=fileCount

    if output == 'y':
        
        # WRITE TO FILE
        indent = ' ' * 4
        count = 0
        writePath = str(path)+'\\file_desc.txt'
        file=open(writePath, 'w')
        file.write('Folder contains the following file types and statistics: \n')

        for key, value in sorted(fileTypes.items()):
            if key not in ['.py']:
                if count == 0:
                    keyval = indent + str(key) + ' : ' + str(value)
                    count = 1
                else:
                    keyval = ','+indent + str(key)+ ' : '+ str(value)
                
                file.write(keyval)

        
        if len(failedTypes) == 0:
            pass
        else:
            file.write('\n\nThe following files do not have an extension: \n')
            for key, value in sorted(failedTypes.items()):
                keyval = indent + str(key)+ ' : '+ str(value) + '\n'
                file.write(keyval)

        
        file.write("\nTotal Files Counted: "+str(fileCountTotal))

        file.write("\nNumber of Unique Extensions: "+str(extCount))

        file.close()

    else:
        pass
        # MISC PRINT STATEMENTS FOR VALUES
        #----------------------------------
        #print fileTypes
        #print failedTypes
        #print failedTypesCount
        #print "Total Files Counted: ",fileCountTotal
        #print "NO EXTENSION FOR: ", failedTypes
        #print "Number of Unique Extensions:",extCount

    return fileTypes

def del_files(path):
    filed = 'file_desc.txt'
    fileS = 'fileStruct.txt'
    foldS = 'foldStruct.txt'
    meta = 'metadata_log.txt'

    check = [filed, fileS, foldS, meta]
    for x in check:
        fileCheck = path +'\\'+ x
        
        if os.path.exists(fileCheck):
            os.remove(fileCheck)
            
        else:
            print x, 'is not a file'
 
startDir = os.getcwd()
 
#count the slashes to get starting depth
startDepth = startDir.count(os.sep)
 
for root, dirs ,files in os.walk(startDir):
 
    #if beyond one level, don't do anything with files, and delete dir references
    #to avoid recursing further
    if root.count(os.sep) - startDepth > 1:
        del dirs[:]
    else:
        for x in dirs:
            path = os.path.join(root,x)
            print path
            del_files(path)
