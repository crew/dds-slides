'''
Twitter Slide

Using: http://python-twitter.googlecode.com
Docs: http://python-twitter.googlecode.com/hg/doc/twitter.html
'''

import clutter
import gobject
import twitter
from crew.dds import baseslide

class TwitterDisplay(baseslide.BaseSlide):
    def __init__(self):
        baseslide.BaseSlide.__init__(self)
        self.twitterAPI = twitter.Api()
        self.username = 'neu_tweet' # The user we're displaying

        # Store their statuses
        self.statuses = self.twitterAPI.GetUserTimeline(self.username)

        # Initalize Shit
        self.setupBackground()
        self.drawStatusList(self.statuses)

#    def event_beforeshow(self):

    # def event_aftershow(self):
    #     None

    # def event_afterhide(self):
    #     self.tm.stop()

    # Setup the background. Duh!
    #
    # setupBackground  Nothing -> Nothing
    def setupBackground(self):
        stageBackground = clutter.Texture('background.png')
        stageBackground.set_position(0, 0)
        self.group.add(stageBackground)

    # Draw the given statuses in the status list.
    #
    # setupBackground  ListofStatuses -> Nothing
    def drawStatusList(self, tweets):
        new_y = 300
        for status in tweets:
            stat_text  = self.add_status_group(status, new_y)
            self.group.add(stat_text)
            new_y = new_y + stat_text.get_height()


    # Add a status to the list on the left. Given
    # a Status object and a Y position.
    #
    # add_status_group  Status Integer -> (Clutter.Text(), Integer)
    def add_status_group(self, status, start_y):
        # Make the clutter actor for the tweet
        stat_text = clutter.Text()
        stat_text.set_font_name("sans serif 18")
        # Pull out the text from the status
        stat_text.set_text(status.text)
        stat_text.set_width(870)
        stat_text.set_ellipsize(3)
        stat_text.set_color(clutter.color_from_string("black"))
        stat_text.set_position(1000, start_y)

        return stat_text


app = TwitterDisplay()
slide = app.group
