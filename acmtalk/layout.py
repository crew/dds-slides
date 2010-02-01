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
        self.event_beforeshow(first=True)

    def draw_bg(self):
        # Draw images
        bg = clutter.Rectangle()
        bg.set_color(clutter.color_from_string('#6a9cd2'))
        bg.set_size(1920, 1080)
        bg.set_position(0, 0)
        bg.set_depth(1)
        self.group.add(bg)
 
        self.sunbeams = clutter.Texture('sunbeams.png')
        self.sunbeams.set_position(-800, -500)
        self.sunbeams.set_depth(2)
        self.group.add(self.sunbeams)

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
   
    def event_beforeshow(self, first=False):
        e = self.pick_event()
        if first:
            self.draw_bg()
            self.setupanimation()
            self.draw_event(e)
        self.fill_event(e)
        self.tm.start()
    
    def event_afterhide(self):
        self.tm.stop()

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

    def fill_event(self, event):
        # Some of these events don't have descriptions or locations associated
        # with them. Set as empty string.
        if not event.has_key('description'):
            event['description'] = ''

        if not event.has_key('location'):
            event['location'] = ''

        self.eventtitle.set_text(event['summary'])
        self.descblock.set_text(event['description'])
        self.dateline.set_text(self.dtstart(event).strftime('%B %e %Y'))
        self.timeline.set_text(self.dtstart(event).strftime('%I:%M %p')
                          + ', ' + event['location'])

    def draw_event(self, event):
        self.eventtitle = clutter.Text()
        self.eventtitle.set_font_name('serif 58')
        self.eventtitle.set_color(clutter.color_from_string('#ffffff'))
        self.eventtitle.set_size(1920, 200)
        self.eventtitle.set_position(10, 290)
        self.eventtitle.set_depth(3)
        self.group.add(self.eventtitle)
 
        self.descblock = clutter.Text()
        self.descblock.set_font_name('serif 24')
        self.descblock.set_color(clutter.color_from_string('#ffffff'))
        self.descblock.set_position(20, 470)
        self.descblock.set_size(1200, 500)
        self.descblock.set_depth(3)
        self.descblock.set_line_wrap(True)
        self.group.add(self.descblock)

        self.dateline = clutter.Text()
        self.dateline.set_font_name('serif 60')
        self.dateline.set_color(clutter.color_from_string('#ffffff'))
        self.dateline.set_position(950, 40)
        self.dateline.set_size(820, 300)
        self.dateline.set_depth(3)
        self.group.add(self.dateline)

        self.timeline = clutter.Text()
        self.timeline.set_font_name('serif 48')
        self.timeline.set_color(clutter.color_from_string('#ffffff'))
        self.timeline.set_position(950, 150)
        self.timeline.set_size(1200, 300)
        self.timeline.set_depth(3)
        self.group.add(self.timeline)

    def setupanimation(self):
        self.tm = clutter.Timeline(duration=200000)
        self.tm.set_loop(True)
        self.alpha = clutter.Alpha(self.tm, clutter.LINEAR)
        self.behaviour = clutter.BehaviourRotate(clutter.Z_AXIS, 0.0, 360.0,
                                                 self.alpha, clutter.ROTATE_CW)
        self.behaviour.set_center(int(self.sunbeams.get_width()/2),
                                  int(self.sunbeams.get_height()/2), 0)
        self.behaviour.apply(self.sunbeams)
    

app = ACMCalendar()
slide = app.group
