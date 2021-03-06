from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from iRiffSync.iRiffClient import iRiffClient

class Command(BaseCommand):
  def handle(self, *args, **options):
    client = iRiffClient()
    page = 0
    while True:
      pageItems = client.getPage(page)
      self.stdout.write("On Page {} found {} items".format(page, len(pageItems)))
      if (len(pageItems) == 0):
        break
      self.savePage(pageItems)
      page += 1
      
  @transaction.atomic
  def savePage(self, items):
    for item in items:
      #TODO: Grab the existing item from the DB and update in case it's needed
      item.save() 
