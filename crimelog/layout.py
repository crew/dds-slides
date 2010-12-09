#!/usr/bin/env python
# vim: set shiftwidth=4 tabstop=4 softtabstop=4 :
"""
A slide for the NUPD Crime Log.
"""

import baseslide
import os
import re
import clutter
import logging
import feedparser
import datetime
import urllib

WEEKDAYS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
TIMES = re.compile('a\.*m\.*$|p\.*m\.*$|[nN]oon\.*$')
FEEDURL = 'http://pipes.yahoo.com/pipes/pipe.run?_id=85b5990d256f3bc93e8f82002a73fa46&_render=rss'

class CrimeLog(baseslide.BaseSlide):
    def __init__(self):
        baseslide.BaseSlide.__init__(self)
        self.our_path = __file__
        self.rss_feed = None
        self.parsed_latest_items = None
        self.setup()
    
    def feed_path(self):
        return os.path.join(os.path.dirname(self.our_path), 'crime.rss')

    def old_feed(self):
        if not os.path.exists(self.feed_path()):
            return True
        now = datetime.datetime.today().isoformat()[:10]
        (year, month, day) = [int(i) for i in now.split('-')]
        now_date = datetime.date(year, month, day)
        current_feed_stats = os.stat(self.feed_path())
        current_feed_datetime = datetime.datetime.fromtimestamp(current_feed_stats[8])
        feed_date = datetime.date(current_feed_datetime.year, current_feed_datetime.month, current_feed_datetime.day)
        delta = datetime.timedelta(7)
        if now_date - feed_date >= delta:
            return True

    def download_fetch_feed(self, feed_url):
        feed_is_old = self.old_feed()
        if feed_is_old:
            logging.debug('Fetching feed URL: %s' % FEEDURL)
            urllib.urlretrieve(FEEDURL, self.feed_path())
        if self.rss_feed is None or feed_is_old:
            self.rss_feed = feedparser.parse(open(self.feed_path()))

    def setup(self):
        self.download_fetch_feed(FEEDURL)
        latest_ugly = self.rss_feed.entries[0].content[0].value.split('\n')
        latest_items = [self.RemoveHTMLTags(i) for i in latest_ugly]
        self.parsed_latest_items = CrimeLogData(latest_items).get_entries()

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
                time = CrimeTime(line)
                time.text = self.content[num + 1]
                self.crime_dates[-1].times.append(time)
            else: continue

    def get_entries(self):
        self._read_data()
        return self.crime_dates

class CrimeDate:
    def __init__(self, date):
        self.date = date
        self.times = []

class CrimeTime:
    def __init__(self, time):
        self.time = time
        self.text = None

"""
#For testing purposes
app = CrimeLog()
for date in app.parsed_latest_items:
    for time in date.times:
        print "%s, %s -- %s\n" % (date.date, time.time, time.text)
"""
