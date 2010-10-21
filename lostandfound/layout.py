import clutter
import baseslide
import config
import gobject


class LostAndFound(baseslide.BaseSlide):

    def __init__(self):
        super(LostAndFound, self).__init__()
        self.background = clutter.Texture('lost_and_found.png')
        self.group.add(self.background)
        self.background.set_size(1920, 1080)
        self.background.set_position(0, 0)
        # The text that says (upstairs)
        t = clutter.Text()
        t.set_font_name("sans serif 96")
        t.set_text("(upstairs)")
        t.set_color(clutter.color_from_string("white"))
        t.set_position(600, 850)
        self.group.add(t)
        self.upstairs = t
        # This is copied from halfunction.
        # Makes the text blink.
        self.tm = None
        self.tm = clutter.Timeline(duration=2000)
        self.tm.set_loop(True)
        self.alpha = clutter.Alpha(self.tm, clutter.EASE_IN_CUBIC)
        self.behaviour = clutter.BehaviourOpacity(alpha=self.alpha,
            opacity_start=0xFF, opacity_end=0x00)
        self.behaviour.apply(t)

    def event_beforeshow(self):
        return True

    def event_aftershow(self):
        self.tm.start()

    def event_beforehide(self):
        pass

    def event_afterhide(self):
        self.tm.stop()


app = LostAndFound()
slide = app.group
