# -*- coding: utf-8 -*-
import sys, time
import urllib
import urllib2
import json
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
      jdata = json.loads(resdata)
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
  coordlist = []

  base = Document()
  kml = base.createElement("kml")
  kml.setAttribute("xmlns", "http://www.opengis.net/kml/2.2")
  base.appendChild(kml)

  doc = base.createElement("Document")
  kml.appendChild(doc)

  for x in result:
    if x["geo"] != None:
      placemark = base.createElement("Placemark")

      name = base.createElement("name")
      nameText = base.createTextNode(chUTC2JST(x['created_at']))
      name.appendChild(nameText)
      placemark.appendChild(name)

      desc = base.createElement("description")
      descText = base.createTextNode(x['text'])
      desc.appendChild(descText)
      placemark.appendChild(desc)

      point = base.createElement("Point")
      coord = base.createElement("coordinates")
      coordText = base.createTextNode(str(x['geo']['coordinates'][1])+","+str(x['geo']['coordinates'][0]))
      coordlist.append(str(x['geo']['coordinates'][1])+","+str(x['geo']['coordinates'][0]))
      coord.appendChild(coordText)
      point.appendChild(coord)
      placemark.appendChild(point)

      doc.appendChild(placemark)

  # Setting Path
  placemark = base.createElement("Placemark")

  name = base.createElement("name")
  nameText = base.createTextNode("Pathway")
  name.appendChild(nameText)
  placemark.appendChild(name)

  desc = base.createElement("description")
  descText = base.createTextNode("This is test pathway")
  desc.appendChild(descText)
  placemark.appendChild(desc)

  lineString = base.createElement("LineString")
  extrude = base.createElement("extrude")
  extrudeNum = base.createTextNode("1")
  extrude.appendChild(extrudeNum)
  tessellate = base.createElement("tessellate")
  tessellateNum = base.createTextNode("1")
  tessellate.appendChild(tessellateNum)
  altitude = base.createElement("altitudeMode")
  altitudeText = base.createTextNode("absolute")
  altitude.appendChild(altitudeText)
  coord = base.createElement("coordinates")
  for x in coordlist:
    coordValue = base.createTextNode(x)
    coord.appendChild(coordValue)
    space = base.createTextNode(" ")
    coord.appendChild(space)

  lineString.appendChild(extrude)
  lineString.appendChild(tessellate)
  lineString.appendChild(altitude)
  lineString.appendChild(coord)

  placemark.appendChild(name)
  placemark.appendChild(desc)
  placemark.appendChild(lineString)

  doc.appendChild(placemark)

  f.write(base.toxml("UTF-8"))
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
