# vim: set shiftwidth=4 tabstop=4 softtabstop=4 :
import clutter
import baseslide
import config
import logging
import urllib
import datetime
import dateutil.parser
import random
import pytz
from icalendar import Calendar

CAL = 'http://www.google.com/calendar/ical/acm@ccs.neu.edu/public/basic.ics'

class ACMCalendar(baseslide.BaseSlide):
    def dtstart(self, vevent):
        return dateutil.parser.parse(str(vevent['dtstart']))

    def dtend(self, vevent):
        return dateutil.parser.parse(str(vevent['dtend']))

    def __init__(self):
        baseslide.BaseSlide.__init__(self)
	    # Grab the .ics and parse it.
        ics = urllib.urlretrieve(CAL, 'cache.ics')
        self.calendar = Calendar.from_string(open('cache.ics', 'rb').read())

        # Draw text and such
        self.content = []
        self.setupslide()

    def draw_bg(self):
        # Draw images
        bg = clutter.Rectangle()
        bg.set_color(clutter.color_from_string('#6a9cd2'))
        bg.set_size(1920, 1080)
        bg.set_position(0, 0)
        bg.set_depth(1)
        self.group.add(bg)
 
        sunbeams = clutter.Texture('sunbeams.png')
        sunbeams.set_position(-800, -500)
        sunbeams.set_depth(2)
        self.group.add(sunbeams)

        acmlogo = clutter.Texture('nuacmlogo.png')
        acmlogo.set_position(50, 50)
        acmlogo.set_depth(3)
        self.group.add(acmlogo)

        skyline = clutter.Texture('skyline_blue.png')
        skyline.set_size(952, 436)
        skyline.set_position(1920-952, 1080-436)
        skyline.set_depth(3)
        self.group.add(skyline)

        stripe = clutter.Rectangle()
        stripe.set_color(clutter.color_from_string('#ffffff'))
        stripe.set_size(1920, 200)
        stripe.set_position(0, 250)
        stripe.set_opacity(30)
        stripe.set_depth(3)
        self.group.add(stripe)
   
    def setupslide(self):
        self.group.remove_all()
        self.draw_bg()
        e = self.pick_event()
        self.draw_event(e)

    def pick_event(self):
        # Filtering out those not occuring within 10 days of now, or that 
        # occured in the past.	
        now = datetime.datetime.now(pytz.utc)
        delta = datetime.timedelta(days=10)
        all_events = []
        for x in self.calendar.walk('vevent'):
            try:
                if self.dtstart(x) > now:
                    all_events.append(x)
            except:
                pass
        e = random.choice(all_events)
        del all_events
        return e

    def purge(self):
        for x in self.content:
            x.unparent()
            x.destroy()
            self.content.remove(x)
        self.content = []

    def draw_event(self, event):
        self.purge()
        # Some of these events don't have descriptions or locations associated with them. Set as empty string.
        if not event.has_key('description'):
            event['description'] = ''

        if not event.has_key('location'):
            event['location'] = ''

        eventtitle = clutter.Text()
        eventtitle.set_text(event['summary'])
        eventtitle.set_font_name('serif 58')
        eventtitle.set_color(clutter.color_from_string('#ffffff'))
        eventtitle.set_size(1920, 200)
        eventtitle.set_position(50, 290)
        eventtitle.set_depth(3)
        self.group.add(eventtitle)
 
        descblock = clutter.Text()
        descblock.set_text(event['description'])
        descblock.set_font_name('serif 24')
        descblock.set_color(clutter.color_from_string('#ffffff'))
        descblock.set_position(20, 470)
        descblock.set_size(1200, 500)
        descblock.set_depth(3)
        descblock.set_line_wrap(True)
        self.group.add(descblock)

        dateline = clutter.Text()
        dateline.set_text(self.dtstart(event).strftime('%B %e %Y'))
        dateline.set_font_name('serif 60')
        dateline.set_color(clutter.color_from_string('#ffffff'))
        dateline.set_position(950, 40)
        dateline.set_size(820, 300)
        dateline.set_depth(3)
        self.group.add(dateline)

        timeline = clutter.Text()
        timeline.set_text(self.dtstart(event).strftime('%I:%M %p')
                          + ', ' + event['location'])
        timeline.set_font_name('serif 48')
        timeline.set_color(clutter.color_from_string('#ffffff'))
        timeline.set_position(950, 150)
        timeline.set_size(1200, 300)
        timeline.set_depth(3)
        self.group.add(timeline)
        logging.debug(self.content)
    

app = ACMCalendar()
slide = app.group
