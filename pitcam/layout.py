import clutter
import logging
import baseslide

class PitcamSlide(baseslide.BaseSlide):
  def __init__ (self):
    baseslide.BaseSlide.__init__(self)

    slideTitle = clutter.Text()
    slideTitle.set_text('the pitcam.')
    slideTitle.set_font_name('serif 71')
    slideTitle.set_color(clutter.color_from_string("#ffffff"))
    slideTitle.set_size(1920, 100)
    slideTitle.set_position(200, 100)
    self.group.add(slideTitle)

    self.newcam = None
    self.oldcam = None
    self.getnew()
    self.getold()

  def setupslide(self):
    self.update()

  def update(self):
    self.getnew()
    self.getold()

  def getcam(self, camattr, url, x, y):
    firsttime = False
    if camattr is None:
      firsttime = True
    camattr = self.GetTextureFromURL(url, camattr)
    camattr.set_position(x, y)
    camattr.set_size(640,480)
    camattr.show()
    if firsttime:
      self.group.add(camattr)

  def getold(self):
    self.getcam(self.oldcam,
                'http://pitcam.ccs.neu.edu/old.jpeg',
                940,
                300)
    logging.info('Done fetching pitcam old')

  def getnew(self):
    self.getcam(self.newcam,
                'http://pitcam.ccs.neu.edu/new.jpeg',
                140,
                300)
    logging.info('Done fetching pitcam new')

app = PitcamSlide()
slide = app.group
