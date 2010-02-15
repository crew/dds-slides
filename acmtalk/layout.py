# vim: set shiftwidth=4 tabstop=4 softtabstop=4 :
import clutter
import baseslide
import config
import logging
import urllib
import datetime
import random

CAL = 'http://www.google.com/calendar/ical/acm@ccs.neu.edu/public/basic.ics'

class ACMCalendar(baseslide.BaseSlide):
    def __init__(self):
        baseslide.BaseSlide.__init__(self)
        self.ourpath = __file__
        self.setup()

    def setup(self):
        self.setupbg()
        self.download_fetch_ical(CAL)
        self.update_calevents()
        self.setuptext()
        self.setupanimation()

    def setupbg(self):
        # Draw images
        bg = clutter.Rectangle()
        bg.set_color(clutter.color_from_string('#6a9cd2'))
        bg.set_size(1920, 1080)
        bg.set_position(0, 0)
        bg.set_depth(1)
        self.group.add(bg)

        self.sunbeams = clutter.Texture('sunbeams.png')
        self.sunbeams.set_position(-800, -500)
        self.sunbeams.set_size(4000, 4000)
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

    def event_beforeshow(self):
        self.set_event(random.choice(self.calevents))

    def event_aftershow(self):
        self.tm.start()

    def event_afterhide(self):
        self.tm.stop()

    def set_event(self, event):
        startdt = event.dtstart.value.astimezone(self.localtime)
        self.eventtitle.set_text(event.summary.value)
        self.descblock.set_text(event.description.value)
        self.dateline.set_text(startdt.strftime('%B %e %Y'))
        self.timeline.set_text('%s, %s'
                               % (startdt.strftime('%I:%M %p'),
                                  event.location.value))

    def setuptext(self):
        self.eventtitle = clutter.Text()
        self.eventtitle.set_font_name('Garuda 62')
        self.eventtitle.set_color(clutter.color_from_string('#ffffff'))
        self.eventtitle.set_size(1920, 200)
        self.eventtitle.set_position(20, 290)
        self.eventtitle.set_depth(3)
        self.group.add(self.eventtitle)

        self.descblock = clutter.Text()
        self.descblock.set_font_name('Garuda 24')
        self.descblock.set_color(clutter.color_from_string('#ffffff'))
        self.descblock.set_position(20, 470)
        self.descblock.set_size(1850, 500)
        self.descblock.set_depth(3)
        self.descblock.set_line_wrap(True)
        self.descblock.set_justify(True)
        self.group.add(self.descblock)

        self.dateline = clutter.Text()
        self.dateline.set_font_name('Garuda 60')
        self.dateline.set_color(clutter.color_from_string('#ffffff'))
        self.dateline.set_position(950, 40)
        self.dateline.set_size(820, 300)
        self.dateline.set_depth(3)
        self.group.add(self.dateline)

        self.timeline = clutter.Text()
        self.timeline.set_font_name('Garuda 48')
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
