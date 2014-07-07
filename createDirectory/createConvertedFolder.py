import os

startDir = os.getcwd()
startDepth = startDir.count(os.sep)
newDir = r'/converted'

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
            #raw_input()
        else:
            print root + '   --  Exists and skipped'
