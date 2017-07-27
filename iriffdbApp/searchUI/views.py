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
  includeRawTitle = request.GET.get('includeRawTitle', False)
  includeDescription = request.GET.get('includeDesc', False)
  query = Q(guessedTitle__icontains=term)

  if includeRawTitle:
    query |= Q(rawName__icontains=term)
  if includeDescription:
    query |= Q(description__icontains=term)
  foundItems = iRiffItem.objects.filter(query)
  return render(request, 'searchUI/results.html', {'riffHost':iRiffClient.Host,'results':foundItems, 'includeRaw': includeRawTitle, 'includeDesc': includeDescription, 'term': term}) 
