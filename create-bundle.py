#!/usr/bin/python

import tarfile
import os
import sys
from glob import glob

try:
  directory =  sys.argv[1]
  os.chdir(directory)
  files = glob('*')
except IndexError:
  print 'usage: create-bundle.py directory'
  sys.exit(1)

if 'manifest.js' in files:
  bundle = tarfile.open("bundle.tar.gz", "w:gz")
  for name in files:
    bundle.add(name)
  bundle.close()
  sys.exit(0)
else:
  print "no manifest file, aborting."
  sys.exit(2)
