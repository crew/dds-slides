import logging
import threading
import clutter
import baseslide
import browser


class WebkitSlide(baseslide.BaseSlide):

    def __init__(self, url):
        super(self.__class__, self).__init__()
        self.url = url
        self.browser = None

    def event_beforeshow(self):
        self.browser = browser.WebBrowser(self.url)
        self.browser.fullscreen()

    def event_aftershow(self):
        pass

    def event_beforehide(self):
        pass

    def event_afterhide(self):
        self.browser.destroy()


app = WebkitSlide('http://pitcam.ccs.neu.edu')
slide = app.group