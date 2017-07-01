from django.core.management.base import BaseCommand

from iRiffSync.iRiffClient import iRiffClient

class Command(BaseCommand):
  def handle(self, *args, **options):
    self.stdout.write("JUST TESTING")
    client = iRiffClient()
    client.getPage(0)
