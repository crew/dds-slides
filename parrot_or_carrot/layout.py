import clutter
import baseslide
import config
import gobject

class ParrotOrCarrot(baseslide.BaseSlide):
    def __init__(self):
        baseslide.BaseSlide.__init__(self)
        self.zoomed = clutter.Texture('redsquare.png')
        self.actual = clutter.Texture('glowtext.png')

        self.group.add(self.redsquare)
        self.group.add(self.malfunction)
        self.setupanimation()

    def event_beforeshow(self):
        self.setupredsquare()

    def event_aftershow(self):
        self.tm.start()

    def event_afterhide(self):
        self.tm.stop()

    def setupredsquare(self):
        XYPOS = 173.5
        self.redsquare.set_size(1575, 733)
        self.redsquare.set_position(XYPOS, XYPOS)
        self.redsquare.set_depth(1)

        self.malfunction.set_size(1575, 733)
        self.malfunction.set_position(XYPOS, XYPOS)
        self.malfunction.set_depth(3)

    def setupanimation(self):
        self.tm = clutter.Timeline(duration=1200)
        self.tm.set_loop(True)
        self.alpha = clutter.Alpha(self.tm, clutter.EASE_IN_CUBIC)
        self.behaviour = clutter.BehaviourOpacity(alpha=self.alpha, opacity_start=250, opacity_end=0x33)
        self.behaviour.apply(self.malfunction)

app = HALfunction()
slide = app.group
