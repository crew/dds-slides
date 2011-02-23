import logging
import threading
import clutter
from crew.dds import baseslide
from crew.dds.contrib.browser import WebkitSlide

app = WebkitSlide('http://www.ccs.neu.edu/home/souvey/mapiframe.html?zoom=21&latitude=42.33854629529398&longitude=-71.09232717179299&kml=http%253A%252F%252Fwww.ccs.neu.edu%252Fhome%252Faldwin%252Fkml%252F102screen.kml')
slide = app.group
