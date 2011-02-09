import clutter
import baseslide
import config
import gobject
from urllib import urlretrieve

class ParrotOrCarrot(baseslide.BaseSlide):
    def __init__(self):
        baseslide.BaseSlide.__init__(self)
        self.zoomed_image = urlretrieve("http://parrotorcarrot.com/dds.php?rn=1337&fresh=true", "/var/tmp/zoomed.jpg")
        self.actual_image = urlretrieve("http://parrotorcarrot.com/dds.php?rn=1337", "/var/tmp/actual.jpg")
        self.zoomed = clutter.Texture('/var/tmp/zoomed.jpg')
        self.actual = clutter.Texture('/var/tmp/actual.jpg')

        self.group.add(self.zoomed)
        self.group.add(self.actual)
        self.setup_animation()

    def event_beforeshow(self):
        self.setup_images()

    def event_aftershow(self):
        self.tm.start()

    def event_afterhide(self):
        self.tm.stop()

    def setup_images(self):
        XYPOS = 173.5
        self.zoomed.set_size(1575, 733)
        self.zoomed.set_position(XYPOS, XYPOS)
        self.zoomed.set_depth(1)

        self.actual.set_size(1575, 733)
        self.actual.set_position(XYPOS, XYPOS)
        self.actual.set_depth(3)

    def setup_animation(self):
        self.tm = clutter.Timeline(duration=1200)
#        self.tm.set_loop(False)
        self.alpha = clutter.Alpha(self.tm, clutter.EASE_IN_CUBIC)
        self.behaviour = clutter.BehaviourOpacity(alpha=self.alpha, opacity_start=250, opacity_end=0)
        self.behaviour.apply(self.zoomed)

app = ParrotOrCarrot()
slide = app.group
