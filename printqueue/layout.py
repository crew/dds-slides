import cairo
import pango
import clutter
import sys
import baseslide
import logging
import urllib
import json
import re

SCREEN_HEIGHT = 1200
SCREEN_WIDTH = 1920

class PrintDisplay(baseslide.BaseSlide):
  def __init__(self, dataURL):
    """ Initializes the stage and score for this slide, using the
        given url to get the printer data. """
    baseslide.BaseSlide.__init__(self)
    # Stores the information for all the elements of each row
    self.rows = list()
    self.dataURL = dataURL
    self.setupmedia()
  
  def setupmedia(self):
    # Background
    self.background = clutter.Texture(filename='background.jpg')
    self.background.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
    self.background.set_position(0, 0)
    self.group.add(self.background)
    # Checkbox media
    self.checkmark = clutter.Texture(filename='checkmark.png')
    self.checkmark.set_size(40, 40)
    self.checkmark.hide()
    self.xmark = clutter.Texture(filename='xmark.png')
    self.xmark.set_size(40, 40)
    self.xmark.hide()
    self.group.add(self.xmark)
    self.group.add(self.checkmark)

  def event_beforeshow(self):
    self.refresh(self.dataURL)
  
  def refresh(self, dataURL):
    self.parsedata(dataURL)
    self.makeslide()
    self.render()

  def event_afterhide(self):
    self.rowContainer.destroy()
    for x in self.rows:
      self.rows.remove(x)
      del x

  def parsedata(self, url):
    """ Parse data from the given URL, and populate data objects
        with that data. """
    # use urllib to grab data from the url we're given
    webjson = urllib.urlopen(url)
    fdata = webjson.read() # the raw JSON from the printserver
    converter = json.JSONDecoder()
    pyjson = converter.decode(fdata)
    self.data = pyjson

  def makeslide(self):
    """ Adds the json print feed information to this slide. """
    headers = {"state":"Status", "owner":"Owner", "title":"Title",
                "physicaldest":"Printer"}

    y = 150
    for entry in self.data["jobs"]:
      if y >= SCREEN_HEIGHT:
        break
      y += self.add_entry_group(entry, y, width=SCREEN_WIDTH) + 12


  def add_entry_group(self, entry, starty, width=SCREEN_WIDTH):

    # a group which stores all the elements of this entry
    # (that is, it stores all the elements
    container = clutter.Group()
    container.set_position(150, starty)
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

    ### CHECKBOX AND MARKS ###

    checkbox = clutter.CairoTexture(width=50, height=50)
    checkbox.set_position(30,10)
    # we obtain a cairo context from the clutter.CairoTexture
    # and then we can use it with the cairo primitives to draw
    # on it.
    context = checkbox.cairo_create()

    # we scale the context to the size of the surface
    context.set_line_width(2)
    context.set_source_color(clutter.color_from_string("black"))
    # This number is in radians and was found by trial&error
    # See: http://en.wikipedia.org/wiki/File:Degree-Radian_Conversion.svg
    context.rotate(6.28)
    self.roundedrec(context, 5, 5, 30, 30, 5)
    context.stroke()

    del(context)

    container.add(checkbox)
    container.show()

    if entry['state'] in ['completed', 'canceled']:
      if entry['state'] == 'completed':
        mark = clutter.Clone(self.checkmark)
      elif entry['state'] == 'canceled':
        mark = clutter.Clone(self.xmark)
      mark.set_position(30, 10)
      mark.set_width(checkbox.get_width() - 7)
      mark.set_height(checkbox.get_height() - 7)
      container.add(mark)

    container.add(statusrect)

    content = clutter.Text()
    content.set_font_name("Georgia 24")
    content.set_text(entry['owner'])
    content.set_use_markup(True)
    content.set_line_wrap(True)
    content.set_line_wrap_mode(2)
    content.set_color(clutter.color_from_string("black"))
    content.set_position(125, 10)
    content.set_width(width)
    content.set_ellipsize(3)
    container.add(content)

    jobtitle = clutter.Text()
    jobtitle.set_font_name("Georgia 22")
    jobtitle.set_markup("<i>%s</i>" % entry["title"])
    jobtitle.set_line_wrap(True)
    jobtitle.set_line_wrap_mode(0)
    jobtitle.set_color(clutter.color_from_string("black"))
    jobtitle.set_position(300, 10)
    jobtitle.set_width(width)
    jobtitle_height = jobtitle.get_height()
    #jobtitle.set_ellipsize(3) #Omit characters at the end of the text
    container.add(jobtitle)


    destination = clutter.Text()
    destination.set_font_name("Georgia 24")
    destination.set_line_wrap(True)
    destination.set_line_wrap_mode(2)
    destnText = ""
    if entry["physicaldest"] == "dali":
      destnText = "<i>%s</i>" % entry["physicaldest"]
    elif entry["physicaldest"] == "Printer":
      destnText = entry["physicaldest"]
    else:
      destnText = "<b>%s</b>" % entry["physicaldest"]
    destination.set_markup(destnText)
    destination.set_position(850, 10)
    destination.set_width(width)
    destination_height = destination.get_height()
    destination.set_ellipsize(3) #Omit characters at the end of the text
    container.add(destination)

    self.rows.append(container)
    return checkbox.get_height()

  def roundedrec(self, context, x, y, w, h, r=10):
    "Draw a rounded rectangle"
    context.move_to(x+r,y)                      # Move to A
    context.line_to(x+w-r,y)                    # Straight line to B
    context.curve_to(x+w,y,x+w,y,x+w,y+r)       # Curve to C, Control points are both at Q
    context.line_to(x+w,y+h-r)                  # Move to D
    context.curve_to(x+w,y+h,x+w,y+h,x+w-r,y+h) # Curve to E
    context.line_to(x+r,y+h)                    # Line to F
    context.curve_to(x,y+h,x,y+h,x,y+h-r)       # Curve to G
    context.line_to(x,y+r)                      # Line to H
    context.curve_to(x,y,x,y,x+r,y)             # Curve to A

  def render(self):
    """Renders the rows and colums from the rows object in this slide."""
    self.rowContainer = clutter.Group()

    # Make the title
    title = "Print Queue for %s" % self.data["status"][2]["name"]
    feedtitleActor = clutter.Text()
    feedtitleActor.set_text(title)
    feedtitleActor.set_font_name("Georgia Bold 42")
    feedtitleActor.set_color(clutter.color_from_string("black"))
    feedtitleActor.set_size(SCREEN_WIDTH, 150)
    feedtitleActor.set_position(290, 50)

    self.rowContainer.add(feedtitleActor)

    for row in self.rows:
      self.rowContainer.add(row)

    # Now rotate the container that holds the rows
    self.rowContainer.move_by(250, 150)
    self.rowContainer.set_rotation(clutter.Z_AXIS, -3, 0, 0, 0)
    self.group.add(self.rowContainer)

app = PrintDisplay("http://queueviewer.ccs.neu.edu/printqueue/102/json/")
slide = app.group
