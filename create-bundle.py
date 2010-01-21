#!/usr/bin/python

import tarfile
import os
import sys
from glob import glob
import logging
import gflags

gflags.DEFINE_boolean('all', False, 'Process all slides')
FLAGS = gflags.FLAGS

logging.basicConfig(level=logging.INFO)

def makeDestinationDirectory(directory):
  destdir = os.path.join('..', '00bundles', directory)
  if not os.path.exists(destdir):
    os.makedirs(destdir)
  return destdir

def makeBundle(directory):
  origdir = os.getcwd()
  try:
    os.chdir(directory)
    files = glob('*')
    if 'manifest.js' in files:
      dest = os.path.join(makeDestinationDirectory(directory), 'bundle.tar.gz')
      bundle = tarfile.open(dest, "w:gz")
      for name in files:
        bundle.add(name)
      bundle.close()
      logging.info('Created bundle for %s in %s' % (directory, dest))
      return True
    else:
      logging.error("no manifest file in \"%s\", aborting." % directory)
      return False
  finally:
    os.chdir(origdir)

def createAllBundles():
  for x in os.listdir('.'):
    if not os.path.isdir(x):
      logging.debug('Skipping non-dir %s' % x)
    elif not os.path.exists(os.path.join(x, 'manifest.js')):
      logging.debug('No manifest in %s' % x)
    else: 
      makeBundle(x)

if __name__ == '__main__':
  args = FLAGS(sys.argv)
  if len(args) != 2 and not FLAGS.all:
    print 'usage: create-bundle.py directory'
    sys.exit(1)
  elif FLAGS.all:
    createAllBundles()
  else:
    makeBundle(args[1])

