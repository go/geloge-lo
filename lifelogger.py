# -*- coding: utf-8 -*-
import sys, time
import urllib
import urllib2
import simplejson
import re
from datetime import datetime
from datetime import timedelta
from xml.dom.minidom import Document

class pytwit:
  def search(self, keyword, lang, size, today):
    url = "http://search.twitter.com/search.json"
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
      jdata = simplejson.loads(resdata)
      result = result + jdata["results"]
  
    return result

def getThumbPic(result):
  q = re.compile("http://twitpic.com")

  for x in result:
    if q.search(x['text']):
      x['text'] = x['text'].replace('http://twitpic.com/', '<br><img src="http://twitpic.com/show/thumb/')
      x['text'] = x['text'] + '">'

def genKML(result, filename):
  f = open(filename, "w")
  coordlist = ""

  base = Document()
  kml = base.createElement("kml")
  kml.setAttribute("xmlns", "http://www.opengis.net/kml/2.2")
  base.appendChild(kml)

  doc = base.createElement("Document")
  kml.appendChild(doc)

  # Add each places
  for x in result:
    if x["geo"] != None:
      placemark = addElement(element="Placemark", textNode=None, parent=doc, base=base)
      addElement(element="name", textNode=chUTC2JST(x['created_at']), parent=placemark, base=base)
      addElement(element="description", textNode=x['text'], parent=placemark, base=base)
      point = addElement(element="Point", textNode=None, parent=placemark, base=base)
      lang = str(x['geo']['coordinates'][0])
      lat = str(x['geo']['coordinates'][1])

      addElement(element="coordinates", textNode=lat+','+lang, parent=point, base=base)
      coordlist = coordlist + lat+","+lang+" "


  # Add Path info
  placemark = addElement(element="Placemark", textNode=None, parent=doc, base=base)
  addElement(element="name", textNode="Pathway", parent=placemark, base=base)
  addElement(element="description", textNode="This is test pathway", parent=placemark, base=base)

  lineString = addElement(element="LineString", textNode=None, parent=placemark, base=base)
  addElement(element="extrude", textNode="1", parent=lineString, base=base)
  addElement(element="tessellate", textNode="1", parent=lineString, base=base)
  addElement(element="altitudeMode", textNode="absolute", parent=lineString, base=base)

  coord = addElement(element="coordinates", textNode=coordlist, parent=lineString, base=base)

  f.write(base.toxml("UTF-8"))
  f.close()
  print "Synced!!"

def addElement(element=None, textNode=None, parent=None, base=None):
      tmpElement = base.createElement(element)
      if textNode:
        tmpTxtNode = base.createTextNode(textNode)
        tmpElement.appendChild(tmpTxtNode)
      parent.appendChild(tmpElement)

      return tmpElement
  
def chUTC2JST(post_time):
  date = datetime.strptime(post_time, "%a, %d %b %Y %H:%M:%S +0000")
  date = date + timedelta(hours=9)

  return date.strftime("%a, %d %b %Y %H:%M:%S +0000")

if __name__ == "__main__":
  keyword = sys.argv[1]
  lang = "ja"
  size = 1500

  path = "/home/go/public_html/maps/"
  '''
  today = {
    'year':datetime.today().strftime("%Y"),
    'month':datetime.today().strftime("%m"),
    'day':datetime.today().strftime("%d")
  }
  '''
  today = {
    'year':'2010',
    'month':'04',
    'day':'09'
  }
  filename = path+today['year']+today['month']+today['day']+".kml"
  filename = "tmp.kml"

  pytwit = pytwit()
  result = pytwit.search(keyword, lang, size, today)

  getThumbPic(result)
  genKML(result, filename)

  '''
  for x in result:
    try:
      print "%s\n%s\n%s\n" % (x["from_user"].encode("utf-8"), x["text"].encode("utf-8"), x["geo"]["coordinates"])
    except:
      print "%s\n%s\n%s\n" % (x["from_user"].encode("utf-8"), x["text"].encode("utf-8"), "None")
  '''
