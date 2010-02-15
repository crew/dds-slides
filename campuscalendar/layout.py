# vim: set shiftwidth=4 tabstop=4 softtabstop=4 :
import clutter
import cairo
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
        baseslide.BaseSlide.__init__(self)
        self.ourpath = __file__
        self.setup()

    def setuptext(self):
        self.eventtitle = clutter.Text()
        self.eventtitle.set_font_name('Baskerville 60')
        self.eventtitle.set_color(clutter.color_from_string('#ffffff'))
        self.eventtitle.set_size(1600, 1)
        self.eventtitle.set_position(125, 225)
        self.eventtitle.set_ellipsize(3)
        self.eventtitle.set_depth(3)
        self.group.add(self.eventtitle)

        self.dateline = clutter.Text()
        self.dateline.set_font_name('Baskerville 52')
        self.dateline.set_color(clutter.color_from_string('#ffffff'))
        self.dateline.set_position(160, 370)
        self.dateline.set_size(250, 1)
        self.dateline.set_depth(3)
        self.group.add(self.dateline)

        self.descblock = clutter.Text()
        self.descblock.set_font_name('Baskerville 24')
        self.descblock.set_color(clutter.color_from_string('#ffffff'))
        self.descblock.set_position(160, 475)
        self.descblock.set_size(1700, 550)
        self.descblock.set_ellipsize(3)
        self.descblock.set_depth(3)
        self.descblock.set_line_wrap(True)
        self.group.add(self.descblock)

    def setupbg(self):
        bg = clutter.Texture('bg.png')
        bg.set_size(1920, 1080)
        bg.set_position(0, 0)
        bg.set_depth(2)
        self.group.add(bg)

        photo = clutter.Texture('photo.jpg')
        photo.set_size(1920, 1080)
        photo.set_position(0, 0)
        photo.set_depth(1)
        self.group.add(photo)

    def setup(self):
        self.download_fetch_ical(CALURL)
        self.update_calevents()
        self.setupbg()
        self.setuptext()

    def event_beforeshow(self):
        self.set_event(random.choice(self.calevents))

    def set_event(self, event):
        startdt = event.dtstart.value.astimezone(self.localtime)
        enddt = event.dtend.value.astimezone(self.localtime)
        start_date = startdt.strftime('%A, %m/%d %I:%M%p')
        end_date = enddt.strftime('%I:%M%p')
        self.eventtitle.set_markup('<span size="larger">%s</span>' % event.summary.value)
        self.dateline.set_markup('<span size="smaller"><i>%s - %s</i></span>' % (start_date, end_date))
        self.descblock.set_markup(event.description.value)

app = CampusCalendar()
slide = app.group
