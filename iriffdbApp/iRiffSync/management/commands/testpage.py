from django.core.management.base import BaseCommand

from iRiffSync.iRiffClient import iRiffClient

class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('page', nargs='+', type=int)

  def handle(self, *args, **options):
    for page in options['page']:
      client = iRiffClient()
      print(client.getPage(page))
