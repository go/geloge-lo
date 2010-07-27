# -*- coding: utf-8 -*-
import re

class Thumbs():
    api_hosts = ["http://twitpic.com", "http://yfrog.com", "http://tweetphoto.com"]

    @classmethod
    def genThumbs(self, text):
        q = [re.compile(url) for url in self.api_hosts]

        if q[0].search(text):
            text = text.replace(self.api_hosts[0], '<br><img src="http://twitpic.com/show/thumb')
            text += '">'
        elif q[1].search(text):
            text = text.replace(self.api_hosts[1], '<br><img src="http://yfrog.com')
            text += '.th.jpg">'
        elif q[2].search(text):
            text = text.replace(self.api_hosts[2], '<br><img width=150 src="http://TweetPhotoAPI.com/api/TPAPI.svc/imagefromurl?size=medium&url='+self.api_hosts[2])
            text += '">'

        return text
