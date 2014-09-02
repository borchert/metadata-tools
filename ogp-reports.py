#!/usr/bin/env python
import glob, os.path, argparse,sys
try:
    from lxml import etree
    XML_LIB = "lxml"
except ImportError:
    try:
        print "\nPython lib lxml not found. Using xml.etree instead. Note that pretty printing with xml.etree is not supported.\n"
        from xml.etree import ElementTree as etree
        XML_LIB = "etree"
    except ImportError:
        print "No xml lib found. Please install lxml lib to continue"

parser = argparse.ArgumentParser()
parser.add_argument("path",help="indicate directory with OGP XMLs to inspect")
parser.add_argument("report_type",help="Indicate a report to run.")
args = parser.parse_args()

REPORT = args.report_type
BASE_PATH = args.path

BASE_PATH = os.path.expanduser(BASE_PATH)

if not os.path.isabs(BASE_PATH):
    BASE_PATH = os.path.abspath(os.path.relpath(BASE_PATH,os.getcwd()))
if os.path.exists(BASE_PATH) == False:
    sys.exit("There's a problem with the inputted path: %s. Are you sure you entered it correctly?" % (BASE_PATH))

if REPORT == "CHECK_ELEMENT":
    elementName = raw_input("What element do you want to check for?: ")
    files = glob.glob(os.path.join(BASE_PATH,"*.xml"))
    for f in files:
        t = etree.parse(f)
        xpath = "*//field[@name='" + elementName +"']"
        if t.find(xpath).text == "UNKNOWN":
            print "Returned UNKNOWN: %s" % (f)
        else:
            print "Returned %s from %s" % (t.find(xpath).text,f)

