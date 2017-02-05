import sys
import urllib.request
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

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
            print(currentItem)
            self.pageItems.append(currentItem)

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

class iRiffItem:
    """Represents an iRiff Item"""
    def __init__(self):
        self.rawName = ""
        self.url = ""
        self.imageRef = ""
        self.price = ""
        self.description = ""

    def __str__(self):
        asString = "iRiffItem\n"
        variables = vars(self)
        for member in variables:
            asString += member+"="+variables[member]+'\n'
        return str(asString.encode(sys.getdefaultencoding(), 'replace'))

if __name__ == '__main__':
    client = iRiffClient()
    client.getPage(0)
