import sys
import urllib.request
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

from iRiffSync.models import iRiffItem

class iRiffClient:
    """Interface to the iRiff listing"""
    baseSearchURL = "/iriffs?solrsort=ds_field_date_released%20desc"
    Host = "http://www.rifftrax.com"

    def __init__(self):
        self.pageItems = []
        
    def getPage(self, pageNo):
        document = self.getElementForSection(iRiffClient.Host+iRiffClient.baseSearchURL+"&page="+str(pageNo))
        iRiffsOnPage = list(document.find(".//div[@class='view-content']"))
        for iRiffOnPage in iRiffsOnPage:
            currentItem = iRiffItem()
            #First the poster
            posterImg = iRiffOnPage.find(".//img[@class='image-style-poster-medium']")
            if posterImg is not None:
                currentItem.imageRef = posterImg.get("src")
            #Then the URL and raw name
            labelEl = iRiffOnPage.find("./div[last()]//a")
            currentItem.url = labelEl.get("href")
            currentItem.rawName = labelEl.text
            self.fillExtraData(currentItem)
            currentItem.guessedTitle = self.guessMovieTitle(currentItem.rawName)
            print(currentItem)
            self.pageItems.append(currentItem)

    def removeSurrounding(self, orig, remove):
      if orig.lower().startswith(remove):
        orig = orig[len(remove):len(orig)]
      if orig.lower().endswith(remove):
        orig = orig[len(orig)-len(remove)]
      return orig.strip()

    def guessMovieTitle(self, rawName):
      #If Present or Presents is here, the title is probably whatever comes after
      #Any words ending in Trax are probably not titles, though this will probably lose me Terror T.R.A.X depending on how they spell it.
      #Phrases after a colon are probably titles, unless they're sequel subtitles.
      guessedName = ""
      for part in rawName.split(" "):
        if not ("riff" in part.lower() or part.lower().endswith("trax")):
          guessedName += part+" "
        elif part.endswith(":"):
          guessedName += ": "
      guessedName = guessedName.strip()
      guessedName = self.removeSurrounding(guessedName, "by")
      guessedName = self.removeSurrounding(guessedName, ":")
      guessedName = self.removeSurrounding(guessedName, "-")
      
      presentIndex = guessedName.lower().find("presents")
      if presentIndex == -1:
        presentIndex = guessedName.lower().find("present")
      if presentIndex != -1:
        nameParts = guessedName.split(" ")
        length = 0
        endOfPresent = 0
        for part in nameParts:
          length += len(part)
          if length > presentIndex:
            return guessedName[length:len(rawName)]

      dashIndex = guessedName.find("-")
      if dashIndex != -1:
        return guessedName[dashIndex+1:len(guessedName)].strip()

      colonIndex = guessedName.find(":")
      if colonIndex != -1:
        guessedName = guessedName[colonIndex+1:len(guessedName)]
      return guessedName.strip()

    def fillExtraData(self, item):
        document = self.getElementForSection(iRiffClient.Host+item.url)
        fields = list(document.find(".//div[@class='region-inner clearfix']"))
        for field in fields:
            fieldClass = field.get("class")
            if "pane-node-product-commerce-price" in fieldClass:
                item.price = ''.join(field.itertext()).strip()
            elif "pane-node-body" in fieldClass:
                item.description = ''.join(field.itertext()).strip()

    def getElementForSection(self, url):
        documentHtml = urllib.request.urlopen(url).read()
        bodyStart = documentHtml.find(b"<section id=\"main-content\">")
        bodyEnd = documentHtml.find(b"</section>",bodyStart)+10
        documentHtml = documentHtml[bodyStart:bodyEnd]
        try:
            return ET.fromstring(documentHtml)
        except ParseError:
            return ET.fromstring(documentHtml+b'</div></div></div></div></div></div></section>')

