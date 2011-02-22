import clutter
import sys
import re
import random
import gobject
import datetime
import os
import urllib
import logging
from crew.dds import baseslide
from crew.dds.contrib import feedparser

class SlashdotDisplay(baseslide.BaseSlide):
  def __init__(self, feedURL):
    """ Initializes the stage and score for this slide. """
    baseslide.BaseSlide.__init__(self)
    self.feedURL = feedURL
    self.rssfeed = None
    self.rssitems = []
    self.titleitems = []
    self.setupBackground()
    self.setupSlider()
    self.addrss(feedURL)

  def setupBackground(self):
    stageBackground = clutter.Texture('background.png')
    stageBackground.set_position(0, 0)
    self.group.add(stageBackground)

  def setupSlider(self):
    self.slider = clutter.Texture('slider.png')
    self.slider.set_position(0,0)
    self.slider.set_opacity(255)
    self.group.add(self.slider)

  def event_beforeshow(self):
    self.refresh()

  def event_loop(self):
    top_story_id = random.randint(0, len(self.item_positions)-1)
    top_entry = self.rssfeed.entries[top_story_id]
    top_story_y = self.item_positions[top_story_id]
    timeline = clutter.Timeline(500)
    alpha = clutter.Alpha(timeline, clutter.LINEAR)
    path = clutter.Path()
    path.add_move_to(945, int(self.slider.get_y()))
    path.add_line_to(945, int(top_story_y-12))
    self.move_slider_behavior = clutter.BehaviourPath(alpha, path)
    self.move_slider_behavior.apply(self.slider)
    timeline.connect('completed', lambda x:
                                  self.update_top_story(top_entry))
    timeline.start()

  def update_top_story(self, top_entry):
    for x in self.titleitems:
       self.group.remove(x)
    self.addTopStory(self.RemoveHTMLTags(top_entry.title),
                     self.RemoveHTMLTags(top_entry.summary))

  def refresh(self):
    for x in self.rssitems:
      self.group.remove(x)
    for x in self.titleitems:
      self.group.remove(x)
    self.addrss(self.feedURL)

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
    self.titleitems.append(title)
    self.group.add(title)
    return title

  def addTopStoryText(self, topstorytext, toptitle):
    content = clutter.Text()
    content.set_text(topstorytext)
    content.set_font_name("serif 21")
    content.set_line_wrap(True)
    content.set_justify(True)
    content.set_line_wrap_mode(2)
    content.set_color(clutter.color_from_string("black"))
    content.set_position(50, 210 + toptitle.get_height())
    content.set_height(1080-260-toptitle.get_height())
    content.set_width(850)
    content.set_ellipsize(3) #Omit characters at the end of the text
    self.group.add(content)
    self.titleitems.append(content)

  def addTopStory(self, title, body):
    self.titleitems = []
    self.addTopStoryText(body.replace("\n", " ").replace(
                            "Read more of this story at Slashdot.", ""),
                         self.addTopStoryTitle(title))

  def feedpath(self):
    return os.path.join(os.path.dirname(__file__), 'slashdot.rss')

  def oldfeed(self):
    if not os.path.exists(self.feedpath()):
      return True
    now = datetime.datetime.now()
    stats = os.stat(self.feedpath())
    lmdate = datetime.datetime.fromtimestamp(stats[8])
    delta = datetime.timedelta(hours=1)
    if not lmdate > (now-delta):
      return True

  def download_fetch_feed(self, feedURL):
    oldfeed = self.oldfeed()
    if oldfeed:
      logging.debug('Fetching feed URL: %s' % feedURL)
      urllib.urlretrieve(feedURL, self.feedpath())
    if self.rssfeed is None or oldfeed:
      self.rssfeed = feedparser.parse(open(self.feedpath()))

  def addrss(self, feedURL):
    """ Adds the RSS feed information to this slide. """
    #TODO: ERROR CHECKING: MAKE SURE WE DON'T EXPLODE WITH A BAD FEED
    self.download_fetch_feed(feedURL)
    self.rssitems = []

    y = 200
    self.item_positions = []
    for entry in self.rssfeed.entries:
      dy, added = self.add_entry_group(entry, y)
      if added:
        self.item_positions.append(y)
        y += dy + 20
      else:
        break

    top_story_id = random.randint(0, len(self.item_positions)-1)
    top_entry = self.rssfeed.entries[top_story_id]
    top_story_y = self.item_positions[top_story_id]
    self.slider.set_position(945, top_story_y-12)
    self.addTopStory(self.RemoveHTMLTags(top_entry.title),
                     self.RemoveHTMLTags(top_entry.summary))

    for x in self.rssitems:
      self.group.add(x)


  def add_entry_group(self, entry, starty):
    topstorytitle = self.RemoveHTMLTags(entry.title)
    title = clutter.Text()
    title.set_font_name("sans serif 18")
    title.set_text(topstorytitle)
    title.set_width(870)
    title.set_ellipsize(3)
    title.set_color(clutter.color_from_string("black"))
    title.set_position(1000, starty)
    #title.set_line_wrap()
    #title.set_line_wrap_mode(2)
    if (title.get_height() + starty + 50) < 1080:
      self.rssitems.append(title)
      return (title.get_height(), True)
    return (title.get_height(), False)

# Put the ClutterGroup containing all the slide information
# in the top level, so that DDS can get at it.
app = SlashdotDisplay("http://rss.slashdot.org/Slashdot/slashdot")
slide = app.group

if __name__ == '__main__':
  app.do_standalone_display()

