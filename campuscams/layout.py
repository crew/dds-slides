import clutter
import logging
import baseslide

# Color ot title text
TITLE_COLOR = "#FFFFFF"
# Positions the pointer can be in
TOP, BOTTOM, LEFT, RIGHT = 1, 2, 3, 4
# Color of border around webcams
BORDER_COLOR = "#AAAACC"
# Width of border surrounding webcams
BORDER_WIDTH = 10
# Webcam picture width
CAM_WIDTH = 370
# Webcam picture height
CAM_HEIGHT = 278

class WebCamera(object):

    def __init__(self, slide, url, x, y, width, height, side=TOP):
        self.slide = slide
        self.url = url
        self.x, self.y = x,y
        self.width, self.height = width, height

        self.decorate(side)
        self.refresh()
        self.slide.group.add(self.texture)

    def decorate(self, pointer_side):
        self.background = clutter.Rectangle()
        self.background.set_color(clutter.color_from_string(BORDER_COLOR))
        self.background.set_size(self.width + 2 * BORDER_WIDTH,
                                 self.height + 2 * BORDER_WIDTH)
        self.background.set_position(self.x - BORDER_WIDTH,
                                     self.y - BORDER_WIDTH)
        self.background.set_depth(0)

        pointer_size = 5 * BORDER_WIDTH
        self.pointer = clutter.Rectangle()
        self.pointer.set_color(clutter.color_from_string(BORDER_COLOR))
        self.pointer.set_size(pointer_size, pointer_size)
        self.pointer.set_depth(0)
        self.pointer.set_anchor_point(pointer_size / 2.0, pointer_size / 2.0)
        self.pointer.set_rotation(clutter.Z_AXIS, 45, 0, 0, 0)
        if pointer_side == TOP:
            self.pointer.set_position(self.x + self.width / 2.0,
                                      self.y - BORDER_WIDTH)
        elif pointer_side == BOTTOM:
            self.pointer.set_position(self.x + self.width / 2.0,
                                      self.y + self.height + BORDER_WIDTH)
        elif pointer_side == LEFT:
            self.pointer.set_position(self.x - BORDER_WIDTH,
                                      self.y + self.height / 2.0)
        else:
            self.pointer.set_position(self.x + self.width + BORDER_WIDTH,
                                      self.y + self.height / 2.0)

        self.slide.group.add(self.background)
        self.slide.group.add(self.pointer)

    def refresh(self):
        self.texture = self.slide.GetTextureFromURL(self.url)
        self.texture.set_position(self.x, self.y)
        self.texture.set_size(self.width, self.height)
        self.texture.set_depth(1)
        self.texture.show()

class CampusCamSlide(baseslide.BaseSlide):
    def __init__ (self):
        baseslide.BaseSlide.__init__(self)
        self.set_map_background()
        self.add_title("Around", 30, 30)
        self.add_title("Northeastern", 50, 130)
        self.add_title("University", 70, 230)

        neu_webcam = "http://155.33.227.163:8080/%s/webcam.jpg"
        locations = [(neu_webcam % 1, 880, 300, TOP),   # Marino Outside
                     (neu_webcam % 2, 1420, 430, TOP),  # QUAD
                     (neu_webcam % 3, 1410, 785, TOP),  # Curry Student Center
                     (neu_webcam % 4, 1300, 15, LEFT),  # Marino Inside
                     (neu_webcam % 5, 262, 776, RIGHT), # Centenial Commons
                     ("http://pitcam.ccs.neu.edu/new.jpeg", 375, 440, TOP)  # New PitCam
        ]
        self.cameras = [WebCamera(self, url, x, y, CAM_WIDTH, CAM_HEIGHT, side)
                        for (url, x, y, side) in locations]
    def beforeshow(self):
        for camera in self.cameras:
            camera.refresh()

    def set_map_background(self):
        map = clutter.Texture('map.png')
        map.set_position(0,0)
        map.set_size(1920, 1080)
        map.set_opacity(80)
        self.group.add(map)

    def add_title(self, text, x, y):
        title = clutter.Text()
        title.set_text(text)
        title.set_font_name('serif 65')
        title.set_color(clutter.color_from_string(TITLE_COLOR))
        title.set_position(x, y)
        title.set_size(1920, 220)
        self.group.add(title)

app = CampusCamSlide()
slide = app.group
