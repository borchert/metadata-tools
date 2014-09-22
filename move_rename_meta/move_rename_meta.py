import os
import shutil
import find_Drive

drivePath = find_Drive.main()

startDir = r'C:\Users\mart3565\Downloads\pub'
outPathDir = os.path.join(drivePath, 'MN Geospatial Commons\\data\\renamed_metadata_xmls')

for root, dirs, files in os.walk(startDir):
    for f in files:
        if f.startswith('meta'):
            filePath = os.path.join(root, f)

            prefix = filePath[38:len(filePath)-22]
            for i in prefix:
                if i == '\\':
                    prefix = prefix.replace(i, '_')

            outFile = os.path.join(outPathDir, prefix + '_metadata.xml')
            if os.path.isfile(outFile):
                print 'REMOVED', outFile
                os.remove(outFile)

            print 'WRITING -', outFile

            shutil.copy(os.path.join(root,f), outFile)