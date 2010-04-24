# -*- coding: utf-8 -*-
import re

api_host = "http://twitpic.com"
def genthumbs(text):
  q = re.compile(api_host)

  if q.search(text):
    text = text.replace(api_host, '<br><img src="http://twitpic.com/show/thumb')
    text += '">'

  return text
