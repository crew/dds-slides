import cairo
import pango
import clutter
import sys
import logging
import urllib
import json
from datetime import timedelta
from crew.dds import baseslide

SCREEN_HEIGHT = 1200
SCREEN_WIDTH = 1920

class UTDisplay(baseslide.BaseSlide):
  def __init__(self, dataURL):
    """ Initializes the stage and score for this slide, using the
        given url to get the uptime data. """
    baseslide.BaseSlide.__init__(self)
    self.dataURL = dataURL
    # Background
    self.background = clutter.Rectangle()
    self.background.set_color(clutter.color_from_string("black"))
    self.background.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
    self.background.set_position(0, 0)

  def event_beforeshow(self):
    self.refresh(self.dataURL)

  def event_loop(self):
    self.refresh(self.dataURL)

  def refresh(self, dataURL):
    self.group.remove_all()
    self.parsedata(dataURL)
    self.makeslide()
    self.render()

  def parsedata(self, url):
    """ Parse data from the given URL, and populate data objects
        with that data. """
    # use urllib to grab data from the url we're given
    webjson = urllib.urlopen(url)
    fdata = webjson.read() # the raw JSON from the server

    converter = json.JSONDecoder()
    pyjson = converter.decode(fdata)

    self.data = pyjson

    # the data has been converted and put into an object...

  def makeslide(self):
    """ Adds the background to this slide. """

    self.group.add(self.background)

  def render(self):
    """Renders the rows and colums from the rows object in this slide."""
    rowContainer = clutter.Group()

    # Server
    titleText = "login.ccs.neu.edu"
    title = clutter.Text()
    title.set_text(titleText)
    title.set_font_name("Monospace Bold 56")
    title.set_color(clutter.color_from_string("white"))
    title.set_position(290, 50)

    rowContainer.add(title)

    # Days
    subtitleText = "<i>%s</i> Days Since Last Downtime"
    subtitleText %= timedelta(seconds=float(self.data["uptime"])).days
    subtitle = clutter.Text()
    subtitle.set_text(subtitleText)
    subtitle.set_use_markup(True)
    subtitle.set_font_name("Monospace 36")
    subtitle.set_color(clutter.color_from_string("white"))
    subtitle.set_position(290, 50+title.get_height())

    rowContainer.add(subtitle)

    self.group.add(rowContainer)

# The bot generating the json lives here
# The code is in crew-misc
app = UTDisplay("http://login.ccs.neu.edu:8099/")
slide = app.group
