import clutter
import logging
import baseslide

class CampusCamSlide(baseslide.BaseSlide):
  def __init__ (self):
    baseslide.BaseSlide.__init__(self)
    self.cam1 = None
    self.cam2 = None
    self.cam3 = None
    self.cam4 = None
    self.cam5 = None
    self.updatecams()

  def beforeshow(self):
    self.updatecams()
  
  def updatecams(self):
    self.getcam(self.cam1, 'http://155.33.227.163:8080/1/webcam.jpg', 202, 174)
    self.getcam(self.cam2, 'http://155.33.227.163:8080/2/webcam.jpg', 774, 174)
    self.getcam(self.cam3, 'http://155.33.227.163:8080/3/webcam.jpg', 1346, 174)
    self.getcam(self.cam4, 'http://155.33.227.163:8080/4/webcam.jpg', 202, 626)
    self.getcam(self.cam5, 'http://155.33.227.163:8080/5/webcam.jpg', 1346, 626)

  def getcam(self, camattr, url, x, y):
    firsttime = False
    if camattr is None:
      firsttime = True
    camattr = self.GetTextureFromURL(url, camattr)
    camattr.set_position(x, y)
    camattr.set_size(370,278)
    camattr.show()
    if firsttime:
      self.group.add(camattr)


app = CampusCamSlide()
slide = app.group
