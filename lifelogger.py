# -*- coding: utf-8 -*-
import sys, time
import urllib
import urllib2
import json
from datetime import datetime
from datetime import timedelta

class pytwit:
  def search(self, keyword, lang, size, today):
    url = "http://search.twitter.com/search.json?"
    result=[]

    for page in range(1,16):
      query = {
        'lang':lang,
        'q':keyword,
        'rpp':100,
        'page':str(page),
        'since':today['year']+"-"+today['month']+"-"+today['day']
      }
      query = urllib.urlencode(query)
      resdata = urllib2.urlopen(url + "?" + query).read()
      jdata = json.loads(resdata)
      result = result + jdata["results"]
  
    return result

def genKML(result, filename):

  f = open(path+filename, "w")
  data = '''<?xml version="1.0" encoding="UTF-8"?>\n
<kml xmlns="http://www.opengis.net/kml/2.2">\n
<Document>\n
  '''
  for x in result:
    if x["geo"] != None:
      data += "<Placemark>\n"
      data += "<name>"
      data += chUTC2JST(x["created_at"])
      data += "</name>\n"
      data += "<description>"
      data += x["text"]
      data += "</description>\n"
      data += "<Point>\n"
      data += "<coordinates>"
      data += str(x["geo"]["coordinates"][1])+","+str(x["geo"]["coordinates"][0])
      data += "</coordinates>\n"
      data += "</Point>\n"
      data += "</Placemark>\n"

  data += "</Document>\n"
  data += "</kml>"
  data = data.encode("utf-8")
  f.write(data)
  f.close()
  print "Synced!!"
  
def chUTC2JST(post_time):
  date = datetime.strptime(post_time, "%a, %d %b %Y %H:%M:%S +0000")
  date = date + timedelta(hours=9)

  return date.strftime("%a, %d %b %Y %H:%M:%S +0000")

if __name__ == "__main__":
  keyword = sys.argv[1]
  lang = "ja"
  size = 1500

  path = "/home/go/public_html/maps/"
  today = {
    'year':datetime.today().strftime("%Y"),
    'month':datetime.today().strftime("%m"),
    'day':datetime.today().strftime("%d")
  }
  filename = today['year']+today['month']+today['day']+".kml"

  pytwit = pytwit()
  result = pytwit.search(keyword, lang, size, today)

  genKML(result, filename)

  '''
  for x in result:
    try:
      print "%s\n%s\n%s\n" % (x["from_user"].encode("utf-8"), x["text"].encode("utf-8"), x["geo"]["coordinates"])
    except:
      print "%s\n%s\n%s\n" % (x["from_user"].encode("utf-8"), x["text"].encode("utf-8"), "None")
  '''
