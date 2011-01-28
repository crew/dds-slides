import cairo
import pango
import clutter
import sys
import baseslide
import logging
import urllib
import json
import re
from time import localtime,strftime,time

SCREEN_HEIGHT = 1200
SCREEN_WIDTH = 1920
TEXT_COLOR = "green"

class IRCDisplay(baseslide.BaseSlide):
  def __init__(self, dataURL):
    """ Initializes the stage and score for this slide, using the
        given url to get the irc data. """
    baseslide.BaseSlide.__init__(self)
    # Stores the information for all the elements of each row
    self.rows = []
    self.dataURL = dataURL
    # Background
    self.background = clutter.Rectangle()
    self.background.set_color(clutter.color_from_string("black"))
    self.background.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
    self.background.set_position(0, 0)

  def event_beforeshow(self):
    self.refresh(self.dataURL)

  def event_loop(self):
    del self.rows
    self.rows = []
    self.refresh(self.dataURL)

  def refresh(self, dataURL):
    self.group.remove_all()
    self.parsedata(dataURL)
    self.makeslide()
    self.render()

  def event_afterhide(self):
    try:
      del self.rows
      self.rows = []
    except:
      logging.exception('encountered error in afterhide')

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
    """ Adds the json irc feed information to this slide. """

    self.group.add(self.background)

    y = 270
    # 14 one-line messages will fill the screen
    # multiple-line messages currently mess this up
    # because they wrap.
    # TODO: show less messages if any wrap
    # (must count starting from most recent, at the end)
    for entry in self.data["chats"][-14:]:
      if y >= SCREEN_HEIGHT:
        break
      y += self.add_entry_group(entry, y, width=SCREEN_WIDTH) + 12

  def add_entry_group(self, entry, starty, width=SCREEN_WIDTH):

    padding = 150
    y = 10

    entry_width = width - (2 * padding)

    # a group which stores all the elements of this entry
    # (that is, it stores all the elements
    container = clutter.Group()
    container.set_position(padding, starty)
    container.set_width(entry_width)

    # make private messages bold
    # (we aren't requiring Python 2.5, so
    #  I can't use the ternary operator)
    msgFont = "Monospace"
    if entry["channel"] == "Private Msg":
      msgFont += " Bold"
    msgFont += " 24"

    prefix = clutter.Text()
    prefixText = "%s <%s>" % (strftime("%H:%M", localtime(entry["time"])),
                              entry["nick"])
    prefix.set_use_markup(False)
    prefix.set_font_name(msgFont)
    prefix.set_text(prefixText)
    prefix.set_color(clutter.color_from_string(TEXT_COLOR))
    prefix.set_position(0, y)
    prefix_width = prefix.get_width()
    container.add(prefix)

    msg = clutter.Text()
    msg.set_font_name(msgFont)
    msgText = entry["msg"]
    msg.set_text(msgText)
    msg.set_line_wrap(True)
    msg.set_line_wrap_mode(0)
    msg.set_color(clutter.color_from_string(TEXT_COLOR))
    msg.set_position(prefix_width+25, y)
    msg.set_width(entry_width-(prefix_width+25))
    msg_height = msg.get_height()
    container.add(msg)

    self.rows.append(container)
    return msg_height

  def render(self):
    """Renders the rows and columns from the rows object in this slide."""
    rowContainer = clutter.Group()

    titleText = "IRC Chat on %s" % self.data["channel"]
    title = clutter.Text()
    title.set_text(titleText)
    title.set_font_name("Monospace Bold 56")
    title.set_color(clutter.color_from_string(TEXT_COLOR))
    title.set_position(290, 50)

    rowContainer.add(title)

    subtitleText = "Join the discussion at <i>%s</i>" % self.data["network"]
    subtitle = clutter.Text()
    subtitle.set_text(subtitleText)
    subtitle.set_use_markup(True)
    subtitle.set_font_name("Monospace 36")
    subtitle.set_color(clutter.color_from_string(TEXT_COLOR))
    subtitle.set_position(290, 50+title.get_height())

    rowContainer.add(subtitle)

    for row in self.rows:
      rowContainer.add(row)
      
    self.group.add(rowContainer)

# the bot generating the json lives here
# the code is in crew-misc
app = IRCDisplay("http://login.ccs.neu.edu:8090/")
slide = app.group
