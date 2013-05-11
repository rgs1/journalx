from django.http import HttpResponse
from models import JournalEntry
import json

def index(request):
    entries = [e.to_dict() for e in JournalEntry.objects.all()]
    return HttpResponse(json.dumps(entries))
