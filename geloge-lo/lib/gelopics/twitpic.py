# -*- coding: utf-8 -*-
import re

api_hosts = ["http://twitpic.com", "http://yfrog.com"]
def genthumbs(text):
  q = [re.compile(url) for url in api_hosts]

  if q[0].search(text):
    text = text.replace(api_hosts[0], '<br><img src="http://twitpic.com/show/thumb')
    text += '">'
  elif q[1].search(text):
    text = text.replace(api_hosts[1], '<br><img src="http://yfrog.com')
    text += '.th.jpg">'

  return text
