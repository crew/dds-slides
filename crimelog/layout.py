#!/usr/bin/env python
# vim: set shiftwidth=4 tabstop=4 softtabstop=4 :
"""
A slide for the NUPD Crime Log.
"""

import os
import re
import baseslide
import clutter
import logging
import feedparser
import datetime
import urllib
import random

WEEKDAYS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
TIMES = re.compile('a\.*m\.*$|p\.*m\.*$|[nN]oon\.*$')
FEEDURL = 'http://huntnewsnu.com/category/crime-log/feed/'

class CrimeLog(baseslide.BaseSlide):
    def __init__(self):
        baseslide.BaseSlide.__init__(self)
        self.rss_feed = None
        self.latest_entries = None
        self.setup()
    
    def feed_path(self):
        return os.path.join(os.path.dirname(__file__), 'crime.rss')

    def old_feed(self):
        if not os.path.exists(self.feed_path()):
            return True
        now = datetime.datetime.today().isoformat()[:10]
        (year, month, day) = [int(i) for i in now.split('-')]
        now_date = datetime.date(year, month, day)
        current_feed_stats = os.stat(self.feed_path())
        current_feed_datetime = datetime.datetime.fromtimestamp(current_feed_stats[8])
        feed_date = datetime.date(current_feed_datetime.year, current_feed_datetime.month, current_feed_datetime.day)
        delta = datetime.timedelta(1)
        if now_date - feed_date >= delta:
            return True

    def download_fetch_feed(self):
        feed_is_old = self.old_feed()
        if feed_is_old:
            logging.debug('Fetching feed URL: %s' % FEEDURL)
            urllib.urlretrieve(FEEDURL, self.feed_path())
        if self.rss_feed is None or feed_is_old:
            self.rss_feed = feedparser.parse(open(self.feed_path()))

    def get_latest_entries(self):
        latest_ugly = self.rss_feed.entries[0].content[0].value.split('\n')
        latest = [self.RemoveHTMLTags(i) for i in latest_ugly]
        self.latest_entries = CrimeLogData(latest).get_entries()

    def setup_text(self):
        self.desc_block = clutter.Text()
        self.desc_block.set_font_name('Baskerville 30')
        self.desc_block.set_color(clutter.color_from_string('#ffffff'))
        self.desc_block.set_position(160, 375)
        self.desc_block.set_size(1700, 550)
        self.desc_block.set_ellipsize(3)
        self.desc_block.set_depth(3)
        self.desc_block.set_line_wrap(True)
        self.group.add(self.desc_block)

        self.date_line = clutter.Text()
        self.date_line.set_font_name('Baskerville 30')
        self.date_line.set_color(clutter.color_from_string('#ffffff'))
        self.date_line.set_position(160, 800)
        self.date_line.set_size(250, 100)
        self.date_line.set_depth(3)
        self.group.add(self.date_line)

    def setup_background(self):
        background = clutter.Texture('background.png')
        background.set_size(1920, 1080)
        background.set_position(0, 0)
        background.set_depth(2)
        self.group.add(background)

        photo = clutter.Texture('photo.jpg')
        photo.set_size(1920, 1080)
        photo.set_position(0, 0)
        photo.set_depth(1)
        self.group.add(photo)
        
    def setup(self):
        self.download_fetch_feed()
        self.get_latest_entries()
        self.setup_background()
        self.setup_text()

    def event_beforeshow(self):
        if not self.latest_entries:
            self.get_latest_entries()
        random_entry = random.choice(self.latest_entries)
        self.set_entry(self.latest_entries.pop(self.latest_entries.index(random_entry)))

    def set_entry(self, entry):
        self.date_line.set_markup('%s, %s' % (entry.date.date, entry.time))
        self.desc_block.set_markup('%s' % entry.text)

class CrimeLogData:
    def __init__(self, content):
        self.content = content
        self.crime_dates = []
    
    def _read_data(self):
        current_date = None
        for num, line in enumerate(self.content):
            if line.startswith(WEEKDAYS):
                current_date = CrimeDate(line)
                self.crime_dates.append(current_date)
            elif re.search(TIMES, line) and len(line.split()) <= 2:
                time = CrimeTime(current_date, line)
                time.text = self.content[num + 1]
                current_date.times.append(time)
            else: continue

    def get_entries(self):
        self._read_data()
        entries = []
        for date in self.crime_dates:
            for time in date.times:
                entries.append(time)
        return entries

class CrimeDate:
    def __init__(self, date):
        self.date = date
        self.times = []

class CrimeTime:
    def __init__(self, date, time):
        self.date = date
        self.time = time
        self.text = None

app = CrimeLog()
slide = app.group

"""
    app = CrimeLog()
    for i in app.latest_entries:
        print i.time, i.text
"""
