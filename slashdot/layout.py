import clutter
import pango
import sys
import cgi
import feedparser
import baseslide
import logging
from htmlentitydefs import name2codepoint
# for some reason, python 2.5.2 doesn't have this one (apostrophe)
name2codepoint['#39'] = 39
# regex lib for stripping HTML tags
import re

class SlashdotDisplay(baseslide.BaseSlide):
  def __init__(self, feedURL):
    """ Initializes the stage and score for this slide. """
    baseslide.BaseSlide.__init__(self)
    self.feedURL = feedURL
    self.rssitems = []

    self.setupBackground()
    self.addrss(feedURL)

  def setupBackground(self):
    stageBackground = clutter.Texture('background.png')
    stageBackground.set_position(0, 0)
    self.group.add(stageBackground)

  def setupslide(self):
    self.refresh(self.feedURL)

  def refresh(self, feedURL):
    for x in self.rssitems:
      self.group.remove(x)
    self.addrss(feedURL)

  def addTopStoryTitle(self, topstorytitle):
    title = clutter.Text()
    title.set_font_name("sans serif 24")
    title.set_text(topstorytitle)
    title.set_markup('<b>%s</b>' % topstorytitle)
    title.set_line_wrap(True)
    title.set_line_wrap_mode(2)
    title.set_width(850)
    title.set_color(clutter.color_from_string("black"))
    title.set_position(50, 200)
    self.rssitems.append(title)
    return title

  def addTopStoryText(self, topstorytext, toptitle):
    content = clutter.Text()
    content.set_text(topstorytext)
    content.set_font_name("serif 21")
    content.set_line_wrap(True)
    content.set_line_wrap_mode(2)
    content.set_color(clutter.color_from_string("black"))
    content.set_position(50, 210 + toptitle.get_height())
    content.set_height(1080-260-toptitle.get_height())
    content.set_width(850)
    content.set_ellipsize(3) #Omit characters at the end of the text
    self.rssitems.append(content)

  def addrss(self, feedURL):
    """ Adds the RSS feed information to this slide. """
    #TODO: ERROR CHECKING: MAKE SURE WE DON'T EXPLODE WITH A BAD FEED
    rssfeed = feedparser.parse(feedURL)
    self.rssitems = []

    y = 0
    for entry in rssfeed.entries:
      if not y:
        y = 200
        toptitle = self.addTopStoryTitle(remove_html_tags(entry.title))
        self.addTopStoryText(remove_html_tags(entry.summary), toptitle)
      elif y >= 1080:
        break
      else:
        y += self.add_entry_group(entry, y) + 20
    
    for x in self.rssitems:
      self.group.add(x)


  def add_entry_group(self, entry, starty):
    topstorytitle = remove_html_tags(entry.title)
    title = clutter.Text()
    title.set_font_name("sans serif 18")
    title.set_text(topstorytitle)
    title.set_width(870)
    title.set_color(clutter.color_from_string("black"))
    title.set_position(1000, starty)
    title.set_line_wrap(True)
    title.set_line_wrap_mode(2)
    if (title.get_height() + starty + 50) < 1080:
      self.rssitems.append(title)
    return title.get_height()# + content.get_height()

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
  app = SlashdotDisplay("http://rss.slashdot.org/Slashdot/slashdot")
  return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))

# Put the ClutterGroup containing all the slide information
# in the top level, so that DDS can get at it.
app = SlashdotDisplay("http://rss.slashdot.org/Slashdot/slashdot")
slide = app.group
