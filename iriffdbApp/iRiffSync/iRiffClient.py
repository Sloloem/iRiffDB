import sys
import urllib.request
from lxml import etree as ET
from lxml.html.soupparser import fromstring
from lxml.etree import tostring

from iRiffSync.models import iRiffItem

class iRiffClient:
    """Interface to the iRiff listing"""
    baseSearchURL = "/iriffs?solrsort=ds_field_date_released%20desc"
    Host = "http://www.rifftrax.com"

    def getPage(self, pageNo):
        #print("Starting to fetch iRiff Page {}.".format(pageNo))
        pageItems = []
        document = self.getElementForSection(iRiffClient.Host+iRiffClient.baseSearchURL+"&page="+str(pageNo))

        iRiffsOnPage = list(document.find(".//div[@class='view-content']") or [])
        print("Found {} iRiff Stubs on this page.".format(len(iRiffsOnPage)))
        for iRiffOnPage in iRiffsOnPage:
            currentItem = iRiffItem()
            #First the poster
            posterImg = iRiffOnPage.find(".//img[@class='image-style-poster-medium']")
            if posterImg is not None:
                currentItem.imageRef = posterImg.get("src")
            #Then the URL and raw name
            labelEl = iRiffOnPage.find("./div[last()]//a")
            currentItem.url = urllib.request.pathname2url(labelEl.get("href"))
            currentItem.rawName = labelEl.text
            #print("Found iRiff ({}) and fetching extra data".format(currentItem.rawName))
            self.fillExtraData(currentItem)
            currentItem.guessedTitle = self.guessMovieTitle(currentItem.rawName)
            pageItems.append(currentItem)
        return pageItems

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
      #print("From original title ({}) and guessed movie title is: {}".format(rawName, guessedName.strip()))
      return guessedName.strip()

    def fillExtraData(self, item):
        document = self.getElementForSection(iRiffClient.Host+item.url)
        fields = list(document.find(".//div[@class='region-inner clearfix']"))
        for field in fields:
            fieldClass = field.get("class")
            if "pane-node-product-commerce-price" in fieldClass:
                item.price = ''.join(field.itertext()).strip().strip('$')
            elif "pane-node-body" in fieldClass:
                item.description = ''.join(field.itertext()).strip()
        if item.price is None:
          print("Found an item with NULL price, assuming $1.99")
          print(iRiffClient.Host+item.url)
          item.price = 1.99
        if item.imageRef == '':
          print("No image ref on list page, using image from item page if available")
          print(iRiffClient.Host+item.url)
          image = document.find(".//img[@class='image-style-poster-medium']")
          if image is not None:
            item.imageRef=image.get('src')

    def getElementForSection(self, url):
      #print("Grabbing from URL ({}) and trying to find main-content.".format(url))
      documentHtml = urllib.request.urlopen(url).read()
      document = fromstring(documentHtml);
      return document.find(".//section[@id='main-content']")

