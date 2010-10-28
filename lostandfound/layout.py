import clutter
import baseslide
import config
import gobject


class LostAndFound(baseslide.BaseSlide):

    def __init__(self):
        super(LostAndFound, self).__init__()
        self.background = clutter.Texture('Lost.jpg')
        self.blurtext = clutter.Texture('Lost-Blur.jpg')

        self.group.add(self.background)
        self.group.add(self.blurtext)
        self.setupanimation()

    def event_aftershow(self):
        self.tm.start()

    def event_afterhide(self):
        self.tm.stop()

    def setupanimation(self):
        self.tm = clutter.Timeline(duration=2500)
        self.tm.set_loop(False)
        self.alpha = clutter.Alpha(self.tm, clutter.EASE_IN_CUBIC)
        self.behaviour = clutter.BehaviourOpacity(alpha=self.alpha, opacity_start=0, opacity_end=250)
        self.behaviour.apply(self.blurtext)

app = LostAndFound()
slide = app.group
