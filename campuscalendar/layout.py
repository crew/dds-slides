# To run as oneslide within slide 5 WD: tar -pvczf bundle.tar.gz .; /opt/local/bin/python2.6 ~/frontend/src/dds.py --oneslide 5
# vim: set shiftwidth=4 tabstop=4 softtabstop=4 :
import clutter
import baseslide
import config
import logging
import urllib
import datetime
import dateutil.parser
from random import choice
from icalendar import Calendar

class CampusCalendar(baseslide.BaseSlide):
    def dtstart(self, vevent):
        return dateutil.parser.parse(str(vevent['dtstart']))

    def dtend(self, vevent):
        return dateutil.parser.parse(str(vevent['dtend']))

    def location(self, vevent):
	      "" if not vevent.has_key('location') else vevent['location']

    def description(self, vevent):
	      vevent['summary'] if not vevent.has_key('description') else vevent['description']

    def __init__(self):
	      self.refresh()

    def event_beforeshow(self):
	      self.refresh()

    def refresh(self):
	      # Grab the .ics and parse it.
        ics = urllib.urlretrieve('http://www.trumba.com/calendars/northeastern-events.ics', 'cache.ics')
        calendar = Calendar.from_string(open('cache.ics', 'rb').read())

        # Filtering out those not occuring within 20 days of now, or that occured in the past.	
        today = datetime.datetime.today()
        delta = datetime.timedelta(days=20)
        all_events = filter(lambda e: (self.dtstart(e) > today) and (self.dtstart(e) < today + delta), calendar.walk('vevent'))

        # Pick an event randomly.
        event = choice(all_events)

        # Some of these events don't have descriptions or locations associated with them. Set as empty string.
        if not event.has_key('description'):
            event['description'] = ''

        if not event.has_key('location'):
            event['location'] = ''

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
        eventtitle.set_text(event['summary'])
        eventtitle.set_font_name('serif 48')
        eventtitle.set_color(clutter.color_from_string('#000'))
        eventtitle.set_size(1600, 1)
        eventtitle.set_position(250, 370)
        eventtitle.set_ellipsize(3)
        eventtitle.set_depth(3)
        self.group.add(eventtitle)
 
        locationline = clutter.Text()
        locationline.set_text(event['location'])
        locationline.set_font_name('serif 24')
        locationline.set_color(clutter.color_from_string('#000'))
        locationline.set_size(1600, 1)
        locationline.set_position(250, 450)
        locationline.set_ellipsize(3)
        locationline.set_depth(3)
        self.group.add(locationline)

        monthline = clutter.Text()
        monthline.set_text(self.dtstart(event).strftime('%b'))
        monthline.set_font_name('serif 24')
        monthline.set_color(clutter.color_from_string('#ffffff'))
        monthline.set_position(100, 400)
        monthline.set_size(250, 370)
        monthline.set_depth(3)
        self.group.add(monthline)

        dayline = clutter.Text()
        dayline.set_text(self.dtstart(event).strftime('%d'))
        dayline.set_font_name('serif 48')
        dayline.set_color(clutter.color_from_string('#ffffff'))
        dayline.set_position(100, 400)
        dayline.set_size(200, 400)
        dayline.set_depth(3)
        self.group.add(dayline)

        descblock = clutter.Text()
        descblock.set_text(event['description'])
        descblock.set_font_name('serif 24')
        descblock.set_color(clutter.color_from_string('#000'))
        descblock.set_position(85, 530)
        descblock.set_size(1800, 400)
        descblock.set_ellipsize(3)
        descblock.set_depth(3)
        descblock.set_line_wrap(True)
        self.group.add(descblock)
    

app = CampusCalendar()
slide = app.group
