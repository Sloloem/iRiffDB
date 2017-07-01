from django.db import models

class iRiffItem(models.Model):
    """Represents an iRiff Item"""
    rawName = models.CharField(max_length=400)
    guessedTitle = models.CharField(max_length=400)
    correctedTitle = models.CharField(max_length=400)
    url = models.URLField()
    imageRef = models.URLField()
    price = models.DecimalField(decimal_places=2,max_digits=5)
    description = models.TextField()
    def __init__(self):
        self.rawName = ""
        self.guessedTitle = ""
        self.correctedTitle = ""
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
