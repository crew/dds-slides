import clutter
import sys
import baseslide
import logging
import urllib # reading json from internet
import json # read json from printserver
from htmlentitydefs import name2codepoint
# for some reason, python 2.5.2 doesn't have this one (apostrophe)
name2codepoint['#39'] = 39
# regex lib for stripping HTML tags
import re

SCREEN_HEIGHT = 1200
SCREEN_WIDTH = 1920

class PrintDisplay(baseslide.BaseSlide):
  def __init__(self, dataURL):
    """ Initializes the stage and score for this slide, using the
        given url to get the printer data. """
    baseslide.BaseSlide.__init__(self)
    self.parsedata(dataURL)
    # Stores the information for all the elements of each row
    self.rows = list()
    self.makeslide()
    self.render()
    self.dataURL = dataURL

  def setupslide(self):
    self.refresh(self.dataURL)
    self.parsedata(self.dataURL)

  def refresh(self, dataURL):
    self.group.remove_all()
    self.parsedata(dataURL)
    self.makeslide()

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


    # Make a white rectangle to give the slide a white background
    # (our current preferred solution)
    background = clutter.Texture(filename="background.jpg")
    background.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
    #background.set_size(3000,2000)
    background.set_position(0, 0)
    self.group.add(background)

    title = "Print Queue for " + self.data["status"][2]["name"]
    feedtitleActor = clutter.Text()
    feedtitleActor.set_text(title)
    feedtitleActor.set_font_name("Garamond 64")
    feedtitleActor.set_color(clutter.color_from_string("black"))
    feedtitleActor.set_size(SCREEN_WIDTH, 150)
    feedtitleActor.set_position(0, 0)
    self.group.add(feedtitleActor)

    headers = {"state":"Status", "owner":"Owner", "title":"Title",
                "physicaldest":"Printer"}

    y = 110
    y += self.add_entry_group(headers, y, width=SCREEN_WIDTH) + 10
    for entry in self.data["jobs"]:
      if y >= SCREEN_HEIGHT:
        break
      y += self.add_entry_group(entry, y, width=SCREEN_WIDTH) + 12


  def add_entry_group(self, entry, starty, width=SCREEN_WIDTH):

    # a group which stores all the elements of this entry
    # (that is, it stores all the elements
    container = clutter.Group()
    container.set_position(50, starty)
    container.set_width(1700)
    container.set_height(60)
    # Add a rectangle that wraps the text indicating the status of
    # the given job
    statusrect = clutter.Rectangle()
    if entry["state"] == "completed":
      statusrect.set_border_color(clutter.color_from_string("white"))
    elif entry["state"] == "processing":
      statusrect.set_color(clutter.color_from_string("orange"))
    else: #probably the title bar, no color needed
      statusrect.set_color(clutter.color_from_string("white"))
    statusrect.set_position(0, 0)


    checkbox = clutter.Texture(filename="box.png")
    checkbox.set_position(30, 10)
    # TODO: Remove the magic numbers and set 1:1 size based on height
    checkbox.set_width(40)
    checkbox.set_height(40)
    checkbox_height = checkbox.get_height()
    container.add(checkbox)

    if entry["state"] == "completed":
      checkmark = clutter.Texture(filename="check.png")
      checkmark.set_position(30, 10)
      checkmark.set_width(checkbox.get_width())
      checkmark.set_height(checkbox.get_height())
      container.add(checkmark)

    container.add(statusrect)

    content = clutter.Text()
    content.set_text(entry["owner"])
    content.set_font_name("Garamond 24")
    content.set_line_wrap(True)
    content.set_line_wrap_mode(2)
    content.set_color(clutter.color_from_string("black"))
    content.set_position(100, 10)
    content.set_width(width)
    content_height = content.get_height()
    content.set_ellipsize(3)
    container.add(content)

    jobtitle = clutter.Text()
    jobtitle.set_text(entry["title"])
    jobtitle.set_font_name("Garamond 24")
    jobtitle.set_line_wrap(True)
    jobtitle.set_line_wrap_mode(2)
    jobtitle.set_color(clutter.color_from_string("black"))
    jobtitle.set_position(300, 10)
    jobtitle.set_width(width)
    jobtitle_height = jobtitle.get_height()
    #jobtitle.set_ellipsize(3) #Omit characters at the end of the text
    container.add(jobtitle)


    destination = clutter.Text()
    destination.set_text(entry["physicaldest"])
    destination.set_font_name("Garamond 24")
    destination.set_line_wrap(True)
    destination.set_line_wrap_mode(2)
    if entry["physicaldest"] == "dali":
      destination.set_color(clutter.color_from_string("blue"))
    elif entry["physicaldest"] == "Printer":
      destination.set_color(clutter.color_from_string("black"))
    else:
      destination.set_color(clutter.color_from_string("red"))
    destination.set_position(1150, 10)
    destination.set_width(width)
    destination_height = destination.get_height()
    destination.set_ellipsize(3) #Omit characters at the end of the text
    container.add(destination)

    # Rotate
    self.rows.append(container)
    # Both items are oriented at the same height;
    # only use the title height here
    return checkbox.get_height()

  def render(self):
    """Renders the rows and colums from the rows object in this slide."""
    rowContainer = clutter.Group()
    for row in self.rows:
      rowContainer.add(row)

    # Now rotate the container that holds the rows
    rowContainer.move_by(175, 150)
    rowContainer.set_rotation(clutter.Z_AXIS, -3, 0, 0, 0)
    self.group.add(rowContainer)

  def getreqwidth(self, element):
    """ Gets the column width needed for the given element. """

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
