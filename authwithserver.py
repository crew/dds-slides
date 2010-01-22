#!/usr/bin/python
import cookielib
import urllib2
import urllib
import getpass
import gflags
import sys
import os
import mimetypes
import time

gflags.DEFINE_string('authcookiefile', '~/.dds/authcookies.dat',
                     'Path to authcookiefile')
gflags.DEFINE_string('baseurl', 'http://dds-master.ccs.neu.edu/dds/',
                     'DDS Server Base URL')
FLAGS = gflags.FLAGS


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
        print e
        print 'Upload Failed, Authentication required!'
        time.sleep(1)
        self.doauth(os.path.join(FLAGS.baseurl, 'accounts', 'login/'))
        return self.post_multipart(url, fields, files, recurse)
    finally:
      self.cookiejar.save()

  def create_slide(self, bundlepath):
    content = open(bundlepath).read()
    fields = [('mode', 'create')]
    files = [('bundle', 'bundle.tar.gz', content)]
    posturl = os.path.join(FLAGS.baseurl, 'cli', 'manage_slide')
    if posturl[-1] != '/':
      posturl += '/'
    try:
      return self.post_multipart(posturl, fields, files)
    except urllib2.HTTPError, e:
      print 'Error encountered %s' % e.read()

  def update_slide(self, id, bundlepath):
    id = int(id)
    content = open(bundlepath).read()
    fields = [('mode', 'update'), ('id', str(id))]
    files = [('bundle', 'bundle.tar.gz', content)]
    posturl = os.path.join(FLAGS.baseurl, 'cli', 'manage_slide')
    if posturl[-1] != '/':
      posturl += '/'
    try:
      return self.post_multipart(posturl, fields, files)
    except urllib2.HTTPError, e:
      print 'Error encountered %s' % e.read()
  
  

if __name__ == '__main__':
  args = FLAGS(sys.argv)
  a = AuthedActivity()
  if len(args) == 3:
    print a.update_slide(args[1], args[2]).read()
  elif len(args) == 2:
    print a.create_slide(args[1]).read()
