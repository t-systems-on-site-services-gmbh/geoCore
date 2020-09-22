#!/usr/bin/env python3

import glob
import zipfile
import os

zipname = "geoCore.zip"
pycache = "__pycache__"
excludes = [ "geoCore\\makeres.bat", "geoCore\\pylintrc"]
additional = ["LICENSE", "README.md"]

files = [f for f in glob.glob("geoCore/**/*.*", recursive=True) if f not in excludes and pycache not in f]

if os.path.exists(zipname):
    os.remove(zipname)
with zipfile.ZipFile(zipname, "x") as myzip:
    for f in files:
        myzip.write(f)
    for f in additional:
        myzip.write(f, "geoCore\\" + f)