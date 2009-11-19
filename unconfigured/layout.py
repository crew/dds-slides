import clutter
import baseslide
import config

class Unconfigured(baseslide.BaseSlide):
    def __init__(self):
        baseslide.BaseSlide.__init__(self)
        title = clutter.Text()
        title.set_text("Unconfigured")
        title.set_font_name("serif 71")
        title.set_color(clutter.color_from_string("gold"))
        title.set_size(1920, 100)
        title.set_position(0, 0)
        self.group.add(title)
        
        jid = config.Option("client-jid")
        jid = jid.split('@')[0]
        unconfigured = ('This client is unconfigured. '
                        'Please use the DDS Master interface to add JID "'
                        '%s'
                        '" to a client group.' % jid)
                        
        message = clutter.Text()
        message.set_text(unconfigured)
        message.set_font_name("serif 48")
        message.set_line_wrap(True)
        message.set_color(clutter.color_from_string("white"))
        message.set_size(1920, 30)
        message.set_position(0, 120)
        self.group.add(message)
        
    
app = Unconfigured()
slide = app.group