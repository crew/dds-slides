import clutter
import baseslide
import config
import gobject
import time
from urllib import urlretrieve

SCREEN_HEIGHT = 1200
SCREEN_WIDTH = 1920

class ParrotOrCarrot(baseslide.BaseSlide):
    def __init__(self):
        baseslide.BaseSlide.__init__(self)

    def event_beforeshow(self):
        self.zoomed_image = urlretrieve("http://parrotorcarrot.com/dds.php?rn=1337&fresh=true", "/var/tmp/zoomed.jpg")
        self.actual_image = urlretrieve("http://parrotorcarrot.com/dds.php?rn=1337", "/var/tmp/actual.jpg")
        self.zoomed = clutter.Texture('/var/tmp/zoomed.jpg')
        self.actual = clutter.Texture('/var/tmp/actual.jpg')

        self.title = clutter.Text()
        self.title.set_text("Parrot or Carrot?")
        self.title.set_font_name("Serif Bold 56")
        self.title.set_color(clutter.color_from_string("white"))

	self.setup_images()
        self.group.add(self.zoomed)
        self.group.add(self.actual)
        self.group.add(self.title)
        self.setup_animation()

    def event_aftershow(self):
        self.tm.start()

    def event_afterhide(self):
        self.tm.stop()

    def setup_images(self):
        XYPOS = 173.5
        self.zoomed.set_size(1575, 733)
        self.zoomed.set_position(XYPOS, XYPOS)
        self.zoomed.set_depth(2)

        self.actual.set_size(1575, 733)
        self.actual.set_position(XYPOS, XYPOS)
        self.actual.set_depth(1)

        self.title.set_position(SCREEN_WIDTH/2-self.title.get_width()/2, 45)
        self.title.set_depth(3)

    def setup_animation(self):
        self.tm = clutter.Timeline(duration=2000)
        self.tm.set_delay(5000) 
        self.alpha = clutter.Alpha(self.tm, clutter.EASE_IN_CUBIC)
        self.behaviour = clutter.BehaviourOpacity(alpha=self.alpha, opacity_start=250, opacity_end=0)
        self.behaviour.apply(self.zoomed)

app = ParrotOrCarrot()
slide = app.group
