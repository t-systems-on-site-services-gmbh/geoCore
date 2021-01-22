#!/usr/bin/env python3

"""Helper script to create the plugin zip-file"""

import glob
import zipfile
import os

ZIPNAME = "geoCore.zip"
PYCACHE = "__pycache__"
excludes = [ "geoCore\\makeres.bat", "geoCore\\pylintrc"]
additional = ["LICENSE", "README.md"]

files = [f for f in glob.glob("geoCore/**/*.*", recursive=True)
    if f not in excludes and PYCACHE not in f]

if os.path.exists(ZIPNAME):
    os.remove(ZIPNAME)
with zipfile.ZipFile(ZIPNAME, "x") as myzip:
    for f in files:
        myzip.write(f)
    for f in additional:
        myzip.write(f, "geoCore\\" + f)
        