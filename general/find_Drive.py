#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------
# find_Drive.py
# Created on: 2014-09-22
# Description: Finds users Drive path.
# ---------------------------------------------------------------------------

# This script finds the users Drive path (if installed).  This is used in many
# of the scripts.

import os

def main():
    userName = os.environ.get('USERNAME')
    if os.path.exists(r'D:\drive\\'):
        drivePath = r'D:\drive\Map_Library_Projects'
    elif os.path.exists(os.path.join(r'C:\Users\\',userName,'Google Drive')):
        drivePath = os.path.join(r'C:\Users\\',userName,'Google Drive\Map_Library_Projects')
    else:
        while True:
            drivePath = raw_input("Please enter the path to your Drive folder (i.e. D:\drive or C:\Users\username\Google "
                                  "Drive):  ")
            if not os.path.exists(drivePath):
                print 'That path does not work.  Please try again.'
            else:
                break

    return drivePath

if __name__ == '__main__':
   main()