import logging
import threading
import clutter
from crew.dds import baseslide
from crew.dds.contrib.browser import WebkitSlide

app = WebkitSlide('http://metrics.ccs.neu.edu/map/lab102/')
slide = app.group
