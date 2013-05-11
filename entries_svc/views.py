from django.core.exceptions import ObjectDoesNotExist
from django.http import \
    HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django import forms
from django.views.decorators.csrf import csrf_exempt
from models import JournalEntry
import json

class EntryForm(forms.Form):
    screenshot = forms.ImageField(required=False)

@csrf_exempt
def index(request):
    if request.POST:
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            e = JournalEntry(title=request.REQUEST['title'],
                             desc=request.REQUEST['desc'],
                             screenshot=form.cleaned_data['screenshot'])
            e.save()
            return HttpResponse(json.dumps(e.to_dict()))
        else:
            return HttpResponseBadRequest('Bad params')
    else:
        entries = [e.to_dict() for e in JournalEntry.objects.all()]
        return HttpResponse(json.dumps(entries))

def entry(request, entry_id):
    try:
        e = JournalEntry.objects.get(id=entry_id)
        return HttpResponse(json.dumps(e.to_dict()))
    except ObjectDoesNotExist:
        return HttpResponseNotFound('Not found')

def screenshot(request, entry_id):
    try:
        e = JournalEntry.objects.get(id=entry_id)
        fh = open(e.screenshot.path, 'rb')
        return HttpResponse(fh, mimetype="image/jpg")
    except ObjectDoesNotExist:
        return HttpResponseNotFound('Not found')
