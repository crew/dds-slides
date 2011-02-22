import logging
import threading
import clutter
from crew.dds import baseslide
from crew.dds.contrib.browser import WebkitSlide

app = WebkitSlide('http://pitcam.ccs.neu.edu')
slide = app.group
