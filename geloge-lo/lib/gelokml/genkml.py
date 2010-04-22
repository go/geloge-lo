# -*- coding: utf-8 -*-
from xml.dom.minidom import Document

def genKML(result, filename):
  f = open(filename, "w")
  coordlist = ""

  base = Document()
  kml = base.createElement("kml")
  kml.setAttribute("xmlns", "http://www.opengis.net/kml/2.2")
  base.appendChild(kml)

  doc = base.createElement("Document")
  kml.appendChild(doc)

  # Add each placemarks
  for tw in result:
    if x["geo"] != None:
      placemark = addElement(element="Placemark", textNode=None, parent=doc, base=base)
      addElement(element="name", textNode=tw['created_at'], parent=placemark, base=base)
      addElement(element="description", textNode=tw['text'], parent=placemark, base=base)
      point = addElement(element="Point", textNode=None, parent=placemark, base=base)
      lang = str(tw['geo']['coordinates'][0])
      lat = str(tw['geo']['coordinates'][1])

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

def addElement(element=None, textNode=None, parent=None, base=None):
      tmpElement = base.createElement(element)
      if textNode:
        tmpTxtNode = base.createTextNode(textNode)
        tmpElement.appendChild(tmpTxtNode)
      parent.appendChild(tmpElement)

      return tmpElement
