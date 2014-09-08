import os
import zipfile
import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument(name="input_path",help="path to start looking in")

#args = parser.parse_args()

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


inputDir = r'C:\Users\mart3565\Downloads\minneapolis'
#inputDir = args.input_path

unzipDir(inputDir)

