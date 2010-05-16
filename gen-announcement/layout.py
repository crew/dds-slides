# vim: set shiftwidth=4 tabstop=4 softtabstop=4 :
# adaptation of the normal campuscalendar slide to handle some
# announcement-type things
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
import json

class CampusCalendar(baseslide.BaseSlide):
    def __init__(self):
        baseslide.BaseSlide.__init__(self)
        self.ourpath = __file__
        self.setup()

    def fetch_data(self):
        obj = json.load(fp=open("data.js"))
        self.name = obj["name"]
        self.body = obj["body"]

    def setuptext(self):
        self.eventtitle = clutter.Text()
        self.eventtitle.set_font_name('Baskerville 60')
        self.eventtitle.set_color(clutter.color_from_string('#ffffff'))
        self.eventtitle.set_size(1600, 1)
        self.eventtitle.set_position(125, 225)
        self.eventtitle.set_ellipsize(3)
        self.eventtitle.set_depth(3)
        self.group.add(self.eventtitle)

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
        self.fetch_data()
        self.update_calevents()
        self.setupbg()
        self.setuptext()

    def event_beforeshow(self):
        self.set_event(random.choice(self.calevents))

    def set_event(self, event):
        self.eventtitle.set_markup('<span size="larger">%s</span>' % self.title)
        self.descblock.set_markup(self.body)

app = CampusCalendar()
slide = app.group
