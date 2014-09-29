import os
import zipfile

import zipfile
try:
    import zlib
    mode= zipfile.ZIP_DEFLATED
except:
    mode= zipfile.ZIP_STORED



def unzipDir(inputDir):
    for root, dirs, files in os.walk(inputDir):
        for f in files:
            if f.endswith('.zip'):
                inFile = os.path.join(root, f)
                print 'Working on', inFile
                outDir = os.path.join(root, f[:-4])
                if not os.path.isdir(outDir):
                    os.mkdir(outDir)
                    print 'Created',outDir
                else:
                    continue

                with zipfile.ZipFile(inFile,'r') as z:
                    z.extractall(outDir)
                print f,'was successful.'

def zipDir(inputDir):
    zipFileName = os.path.join(inputDir,'zipfile.zip')
    print zipFileName
    zip= zipfile.ZipFile(zipFileName, 'w', mode)
    for root, dirs, files in os.walk(inputDir):
        for f in files:
            if f.endswith('.xml'):
                fileName = os.path.join(root,f)
                zip.write(fileName, arcname=f)
    print 'ZIP CREATED'
    zip.close()


inputDir = r'C:\Users\mart3565\Desktop\test'
#inputDir = args.input_path

#unzipDir(inputDir)
zipDir(inputDir)
