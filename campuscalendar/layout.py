# vim: set shiftwidth=4 tabstop=4 softtabstop=4 :
import clutter
import baseslide
import config
import logging
import urllib
import datetime
import random
import vobject
import pytz

CALURL='http://www.trumba.com/calendars/northeastern-events.ics'

class CampusCalendar(baseslide.BaseSlide):
    def __init__(self):
        self.calendar = None
        self.events = None
        self.refresh()

    def event_beforeshow(self):
        self.refresh()

    def download_parse(self):
        if self.calendar is None:
            tmpfilename = 'cache.ics'
            ics = urllib.urlretrieve(CALURL, tmpfilename)
            self.calendar = vobject.readOne(open(tmpfilename).read())

    def filter_events(self):
        """Filter events not occuring within 20 days of now."""
        today = datetime.datetime.now(pytz.timezone('US/Eastern'))
        delta = datetime.timedelta(days=20)

        self.events = []

        for event in self.calendar.components():
	        if (hasattr(event, 'description') and
					    hasattr(event, 'summary') and
					    hasattr(event, 'location') and
				      hasattr(event.dtstart.value, 'hour') and
				      event.dtstart.value >= today and
				      event.dtstart.value <= (today + delta) and
					    len(event.description.value) >= 100):
				      self.events.append(event)

    def refresh(self):
        self.download_parse()
        self.filter_events()
        event = random.choice(self.events)

        start_date = datetime.datetime.strftime(event.dtstart.value, '%A, %m/%d %I:%M%p')
        end_date = datetime.datetime.strftime(event.dtend.value, '%I:%M%p')

        baseslide.BaseSlide.__init__(self)
        bg = clutter.Texture('bg.png')
        bg.set_size(1920, 1080)
        bg.set_position(0, 0)
        bg.set_depth(2)
        self.group.add(bg)

        bg = clutter.Texture('photo.jpg')
        bg.set_size(1920, 1080)
        bg.set_position(0, 0)
        bg.set_depth(1)
        self.group.add(bg)

        eventtitle = clutter.Text()
        eventtitle.set_text(event.summary.value)
        eventtitle.set_font_name('Large Frys 48')
        eventtitle.set_color(clutter.color_from_string('#ffffff'))
        eventtitle.set_size(1600, 1)
        eventtitle.set_position(100, 200)
        eventtitle.set_ellipsize(3)
        eventtitle.set_depth(3)
        self.group.add(eventtitle)

        dateline = clutter.Text()
        dateline.set_text('<i>' + start_date + ' - ' + end_date + '</i>')
        dateline.set_font_name('Large Frys 36')
        dateline.set_use_markup(True)
        dateline.set_color(clutter.color_from_string('#ffffff'))
        dateline.set_position(100, 300)
        dateline.set_size(250, 1)
        dateline.set_depth(3)
        self.group.add(dateline)

        descblock = clutter.Text()
        descblock.set_text(event.description.value)
        descblock.set_font_name('serif 24')
        descblock.set_color(clutter.color_from_string('#ffffff'))
        descblock.set_position(100, 450)
        descblock.set_size(1700, 550)
        descblock.set_ellipsize(3)
        descblock.set_depth(3)
        descblock.set_line_wrap(True)
        self.group.add(descblock)


app = CampusCalendar()
slide = app.group
