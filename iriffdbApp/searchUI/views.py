from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q

from iRiffSync.models import iRiffItem
from iRiffSync.iRiffClient import iRiffClient

def index(request):
  return render(request, 'searchUI/index.html', {})
def search(request):
  term = request.GET.get('q', '')
  includeRawTitle = request.GET.get('rawTitle', False)
  includeDescription = request.GET.get('description', False)
  foundItems = iRiffItem.objects.filter(
    Q(guessedTitle__icontains=term) #|
    #Q(rawName__icontains=term) if includeRawTitle else Q(False) |
    #Q(description__icontains=term) if includeDescription else Q(False))
    )
  return render(request, 'searchUI/results.html', {'riffHost':iRiffClient.Host,'results':foundItems}) 
