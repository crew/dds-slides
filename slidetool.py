#!/usr/bin/env python
"""Utility for managing slides.

  * Get a list of slides on the server:
  $ ./slidetool.py list

  * Generate a bundle for a given slide directory
  $ ./slidetool.py bundle slidedirectory

  * Generate bundles for all slide directories
  $ ./slidetool.py allbundle

  * Upload a new slide
  $ ./slidetool.py upload bundle.tar.gz

  * Update a pre-existing slide id #5
  $ ./slidetool.py update 5 bundle.tar.gz

*******************************************************************
NOTE! You can run $ ./slidetool.py --help to get other option help.

"""

__author__ = 'Will Nowak <wan@ccs.neu.edu'

import os
import sys
import gflags

import cookielib
import urllib2
import urllib
import getpass
import mimetypes
import time

import tarfile
from glob import glob
import logging
import json

gflags.DEFINE_string('authcookiefile', '~/.dds/authcookies.dat',
                     'Path to authcookiefile')
gflags.DEFINE_string('baseurl', 'http://dds-dev.ccs.neu.edu/dds/',
                     'DDS Server Base URL')
FLAGS = gflags.FLAGS
logging.basicConfig(level=logging.INFO)


class AuthedActivity(object):
  def __init__(self):
    self.setupcookies()

  def cookiefile(self):
    return os.path.expanduser(FLAGS.authcookiefile)

  def setupcookies(self):
    self.cookiejar = cookielib.MozillaCookieJar(filename=self.cookiefile())
    handler = urllib2.HTTPCookieProcessor(self.cookiejar)
    rhandler = urllib2.HTTPRedirectHandler()
    self.opener = urllib2.build_opener(handler)
    self.opener.add_handler(rhandler)

  def loadcookies(self):
    try:
      self.cookiejar.load()
    except:
      dirs = os.path.dirname(self.cookiefile())
      if not os.path.exists(dirs):
        os.makedirs(dirs)
      else:
        self.cookiejar.save()

  def doauth(self, loginurl):
    print 'Login required! Please provide Django Creds.'
    username = raw_input('Username: ')
    password = getpass.getpass('Password: ')
    self.geturl(loginurl, {'username':username, 'password':password},
                recurse=False)

  def geturl(self, url, postdict=None, recurse=True):
    self.loadcookies()
    try:
      pd = None
      if postdict is not None:
        pd = urllib.urlencode(postdict)
      f = self.opener.open(url, pd)
      returnedurl = f.geturl()
      if '/accounts/login/' in returnedurl and recurse:
        self.doauth(returnedurl)
        return self.geturl(url, postdict)
      else:
        return f
    finally:
      self.cookiejar.save()

  def encode_multipart_formdata(self, fields, files):
    """From: http://code.activestate.com/recipes/146306/
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be
    uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
      L.append('--' + BOUNDARY)
      L.append('Content-Disposition: form-data; name="%s"' % key)
      L.append('')
      L.append(value)
    for (key, filename, value) in files:
      L.append('--' + BOUNDARY)
      L.append('Content-Disposition: form-data; name="%s"; filename="%s"'
               % (key, filename))
      L.append('Content-Type: %s' % self.get_content_type(filename))
      L.append('')
      L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

  def get_content_type(self, filename):
    """From: http://code.activestate.com/recipes/146306/"""
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

  def post_multipart(self, url, fields, files, recurse=True):
    self.loadcookies()
    try:
      try:
        content_type, body = self.encode_multipart_formdata(fields, files)
        headers = {'Content-type': content_type,
        'Content-length': str(len(body))}
        req = urllib2.Request(url, body, headers)
        time.sleep(0.1)
        f = self.opener.open(req)
        time.sleep(0.1)

        returnedurl = f.geturl()
        if '/accounts/login/' in returnedurl and recurse:
          self.doauth(returnedurl)
          return self.post_multipart(url, fields, files, recurse)
        else:
          return f
      except Exception, e:
        code = False
        try:
          code = e.code
        except:
          pass
        if code:
          print 'Server failure!'
          print '------------------------------------------'
          print e.read()
          return
        else:
          print e
          print 'Upload Failed, Authentication required!'
          time.sleep(1)
          self.doauth(os.path.join(FLAGS.baseurl, 'accounts', 'login/'))
          return self.post_multipart(url, fields, files, recurse)
    finally:
      self.cookiejar.save()

  def get_slide_listing(self):
    d = self.geturl(os.path.join(FLAGS.baseurl, 'cli', 'list_slides/'))
    sl =  json.load(d)
    o = []
    keys = ['title', 'id', 'owner']
    o.append(keys)
    o.append(('*****', '**', '*****'))
    for x in sl:
      r = []
      for y in keys:
        r.append(x[y])
      o.append(r)
    return o

  def create_slide(self, bundlepath):
    content = open(bundlepath).read()
    fields = [('mode', 'create')]
    files = [('bundle', 'bundle.tar.gz', content)]
    posturl = os.path.join(FLAGS.baseurl, 'cli', 'manage_slide/')
    try:
      return self.post_multipart(posturl, fields, files)
    except urllib2.HTTPError, e:
      print 'Error encountered %s' % e.read()

  def update_slide(self, id, bundlepath):
    id = int(id)
    content = open(bundlepath).read()
    fields = [('mode', 'update'), ('id', str(id))]
    files = [('bundle', 'bundle.tar.gz', content)]
    posturl = os.path.join(FLAGS.baseurl, 'cli', 'manage_slide/')
    try:
      return self.post_multipart(posturl, fields, files)
    except urllib2.HTTPError, e:
      print 'Error encountered %s' % e.read()


class ManifestValidator(object):
  def __init__(self, manifestpath):
    self.path = manifestpath
    self.m = json.load(open(manifestpath))
    self.ok = True

  def errormsg(self, err):
    logging.error('%s in "%s"' % (err, self.path))
    self.ok = False

  def field_exists(self, name):
    if name not in self.m:
      self.errormsg('Field %s missing' % name)
      return False
    else:
      return True

  def field_has_values(self, name, values):
    if self.field_exists(name):
      if self.m[name] not in values:
        self.errormsg('Field %s needs to be one of %s' % (name, str(values)))

  def validate(self):
    self.ok = True
    self.field_has_values('transition', ['fade'])
    self.field_has_values('mode', ['module', 'layout'])
    self.field_has_values('priority', range(11))
    self.field_has_values('duration', range(5, 61))
    self.field_exists('title')
    if self.field_exists('thumbnail_img'):
      if not os.path.exists(self.m['thumbnail_img']):
        self.errormsg('thumbnail_img defined but "%s" does not exist'
                      % self.m['thumbnail_img'])
    return self.ok


def validateManifest(manifestpath):
  m = ManifestValidator(manifestpath)
  return m.validate()

def makeDestinationDirectory(directory):
  destdir = os.path.join('..', '00bundles', directory)
  if not os.path.exists(destdir):
    os.makedirs(destdir)
  return destdir

def makeBundle(directory):
  origdir = os.getcwd()
  try:
    logging.info('Attempting to bundle %s' % directory)
    os.chdir(directory)
    os.system('/usr/bin/env git clean -f -x')
    files = glob('*')
    if 'manifest.js' not in files:
      logging.error("no manifest file in \"%s\", aborting." % directory)
      return False
    elif not validateManifest('manifest.js'):
      logging.error('bad manifest file, aborting')
      return False
    else:
      dest = os.path.join(makeDestinationDirectory(directory), 'bundle.tar.gz')
      bundle = tarfile.open(dest, "w:gz")
      for name in files:
        bundle.add(name)
      bundle.close()
      logging.info('Created bundle for %s in %s' % (directory, dest))
      return True
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

def usage(foo=''):
  print __doc__
  sys.exit(2)

# From
# http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/
def get_max_width(table, index):
  """Get the maximum width of the given column index"""
  return max([len(str(row[index])) for row in table])

# From
# http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/
def pprint_table(out, table):
  """Prints out a table of data, padded for alignment
  @param out: Output stream (file-like object)
  @param table: The table to print. A list of lists.
  Each row must have the same number of columns. """
  col_paddings = []

  for i in range(len(table[0])):
      col_paddings.append(get_max_width(table, i))

  for row in table:
      # left col
      print >> out, row[0].ljust(col_paddings[0] + 1),
      # rest of the cols
      for i in range(1, len(row)):
          col = str(row[i]).rjust(col_paddings[i] + 2)
          print >> out, col,
      print >> out


if __name__ == '__main__':
  args = FLAGS(sys.argv)
  mode = ''
  if len(args) < 2:
    usage(args)
  args = args[1:]
  mode = str(args[0])
  a = AuthedActivity()
  try:
    if mode == 'bundle' and len(args) == 2:
      param = args[1]
      makeBundle(param)
    elif mode == 'allbundle' and len(args) == 1:
      print 'Creating all bundles'
      createAllBundles()
    elif mode == 'update' and len(args) == 3:
      id = int(args[1])
      bundle = args[2]
      print 'Updating #%d with %s' % (id, bundle)
      print a.update_slide(id, bundle).read()
    elif mode == 'upload' and len(args) == 2:
      bundle = args[1]
      print 'Uploading new instance of %s' % bundle
      print a.create_slide(bundle).read()
    elif mode == 'list' and len(args) == 1:
      slides = a.get_slide_listing()
      pprint_table(sys.stdout, slides)
    else:
      raise Exception, 'No commands matched'
  except Exception, e:
    print e
    usage()
