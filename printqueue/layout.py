import clutter
import pango
import sys
import cgi
import baseslide
import logging
import urllib # reading json from internet
import json # read json from printserver
from htmlentitydefs import name2codepoint
# for some reason, python 2.5.2 doesn't have this one (apostrophe)
name2codepoint['#39'] = 39
# regex lib for stripping HTML tags
import re

SCREEN_HEIGHT = 1024
SCREEN_WIDTH = 1280

class PrintDisplay(baseslide.BaseSlide):
  def __init__(self, dataURL):
    """ Initializes the stage and score for this slide, using the
        given url to get the printer data. """
    baseslide.BaseSlide.__init__(self)
    self.parsedata(dataURL)
    self.makeslide()
    self.dataURL = dataURL

  def setupslide(self):
    self.refresh(self.dataURL)
    self.parsedata(dataURL)

  def refresh(self, dataURL):
    self.group.remove_all()
    

  def parsedata(self, url):
    """ Parse data from the given URL, and populate data objects
        with that data. """ 
   # use urllib to grab data from the url we're given
    webjson = urllib.urlopen(url)
    fdata = webjson.read() # the raw JSON from the printserver
    
    converter = json.JSONDecoder()
    pyjson = converter.decode(fdata)

    self.data = pyjson

    # the data has been converted and put into an object...

  def makeslide(self):
    """ Adds the json print feed information to this slide. """
    title = "Print Queue for " + self.data["status"][0]["name"]
    feedtitleActor = clutter.Text()
    feedtitleActor.set_text(title)
    feedtitleActor.set_font_name("serif 62")
    feedtitleActor.set_color(clutter.color_from_string("white"))
    feedtitleActor.set_size(SCREEN_WIDTH, 100)
    feedtitleActor.set_position(0, 0)
    self.group.add(feedtitleActor) 

    y = 100
    for entry in self.data["jobs"]:
      if y >= SCREEN_HEIGHT:
        break
      y += self.add_entry_group(entry, y, width=1280) + 20


  def add_entry_group(self, entry, starty, width=1280):
    title = clutter.Text()
    title.set_font_name("serif 16")
    title.set_text(entry["id"].__str__())
    title.set_markup('<span underline="single">%s</span>' % entry["id"])
    title.set_width(width)
    title.set_color(clutter.color_from_string("white"))
    title.set_position(25, starty)
    self.group.add(title)

    content = clutter.Text()
    content.set_text(entry["owner"])
    content.set_font_name("serif 16")
    content.set_line_wrap(True)
    content.set_line_wrap_mode(2)
    content.set_color(clutter.color_from_string("white"))
    content.set_position(150, starty)
    content.set_width(width)
    content_height = content.get_height()
    content.set_ellipsize(3) #Omit characters at the end of the text
    self.group.add(content)

    status = clutter.Text()
    status.set_text(entry["state"])
    status.set_font_name("serif 16")
    status.set_line_wrap(True)
    status.set_line_wrap_mode(2)
    if entry["state"] == "completed":
      status.set_color(clutter.color_from_string("green"))
    else:
      status.set_color(clutter.color_from_string("orange"))
    
    status.set_position(250, starty)
    status.set_width(width)
    status_height = status.get_height()
    status.set_ellipsize(3) #Omit characters at the end of the text
    self.group.add(status)

    # Both items are oriented at the same height; only use the title height here

    return title.get_height()

def addBackground(self):
  stageBackground = clutter.Texture('feedimage.png')
  stageBackground.set_position(0, 0)
  self.group.add(stageBackground)

def unescape(s):
  """ Replaces HTML entities with their unicode equivalent"""
  # unescape HTML code refs; c.f. http://wiki.python.org/moin/EscapingHtml
  return re.sub('&(%s);' % '|'.join(name2codepoint),
            lambda m: unichr(name2codepoint[m.group(1)]), s)

def remove_html_tags(data):
  """ Removes HTML tags and unscapes the given string. """
  p = re.compile(r'<.*?>')
  return unescape(p.sub('', data))

def main(args=None):
  app = PrintDisplay("http://queueviewer.ccs.neu.edu/printqueue/102/json/")
  return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))

# Put the ClutterGroup containing all the slide information
# in the top level, so that DDS can get at it.
app = PrintDisplay("http://queueviewer.ccs.neu.edu/printqueue/102/json/")
#app = RSSDisplay("http://feeds.digg.com/digg/popular.rss")

slide = app.group
