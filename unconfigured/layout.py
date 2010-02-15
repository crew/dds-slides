import clutter
import baseslide
import config
from threading import Timer

class Unconfigured(baseslide.BaseSlide):
    def __init__(self):
        baseslide.BaseSlide.__init__(self)
        # Images
        self.bg = clutter.Texture('bg.png')
        self.blueprint = clutter.Texture('blueprint.png')
        self.group.add(self.bg)
        self.group.add(self.blueprint)
        # Text
        self.title = clutter.Text()
        self.message = clutter.Text()
        self.group.add(self.title)
        self.group.add(self.message)

    def event_beforeshow(self):
        self.setupbg()
        self.setuptext()

    def event_aftershow(self):
        t = Timer(5.0, self.animateitems)
        t.start()

    def setupbg(self):
        self.bg.set_size(1920, 1080)
        self.bg.set_position(0, 0)
        self.bg.set_depth(1)

        self.blueprint.set_size(1920, 1080)
        self.blueprint.set_position(0, 0)
        self.blueprint.set_depth(3)


    def setuptext(self):
        # Title
        self.title.set_markup("<b>This client is unconfigured</b>")
        self.title.set_font_name("sans 32")
        self.title.set_color(clutter.color_from_string("white"))
        self.title.set_size(1920, 100)
        self.title.set_position(550, 740)
        self.title.set_depth(2)

        # Message
        jid = config.Option("client-jid")
        jid = jid.split('@')[0]
        unconfigured = ('Please use the DDS Web interface to add JID '
                        '<i>%s</i>'
                        ' to a client group.' % jid)

        self.message.set_markup(unconfigured)
        self.message.set_font_name("sans 24")
        self.message.set_line_wrap(True)
        self.message.set_color(clutter.color_from_string("white"))
        self.message.set_size(1400, 30)
        self.message.set_position(300, 800)
        self.message.set_depth(2)
        # Show it when the animation happens
        self.message.hide()


    def animateitems(self):
        self.blueprint.animate(clutter.EASE_OUT_SINE, 500, "width", 960, "height", 540, "x", 455, "y", 150)
        self.message.show()


app = Unconfigured()
slide = app.group
