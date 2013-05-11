from django.core.exceptions import ObjectDoesNotExist
from django.http import \
    HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django import forms
from django.views.decorators.csrf import csrf_exempt
from models import JournalEntry
import json

class EntryForm(forms.Form):
    screenshot = forms.ImageField(required=False)

def _bad_response(msg):
    response = {'error': msg}
    return HttpResponseBadRequest(json.dumps(response))

def _good_response(msg):
    response = {'message': msg}
    return HttpResponse(json.dumps(response))

def _json_response(obj):
    return HttpResponse(json.dumps(obj))

def _get_entry(entry_id):
    try:
        return JournalEntry.objects.get(id=entry_id)
    except ObjectDoesNotExist:
        return None

def _get_comment(e, comment_id):
    try:
        return e.comment_set.get(id=comment_id)
    except ObjectDoesNotExist:
        return None

@csrf_exempt
def index(request):
    if request.POST:
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            e = JournalEntry(title=request.REQUEST['title'],
                             desc=request.REQUEST['desc'],
                             screenshot=form.cleaned_data['screenshot'])
            e.save()
            return _json_response(e.to_dict())
        else:
            return _bad_response('Bad params')
    else:
        entries = [e.to_dict() for e in JournalEntry.objects.all()]
        return _json_response(entries)

@csrf_exempt
def comments_index(request, entry_id):
    e = _get_entry(entry_id)
    if e is None:
        return _bad_response('Entry not found')

    if request.method == 'POST':
        c = e.comment_set.create(text=request.REQUEST['text'])
        return _json_response(c.to_dict())
    else:
        comments = [ c.to_dict() for c in e.comment_set.all()]
        return _json_response(comments)

@csrf_exempt
def comment(request, entry_id, comment_id):
    if request.method != 'DELETE':
        return _bad_response('Bad request')

    e = _get_entry(entry_id)
    if e is None:
        return _bad_response('Entry not found')

    c = _get_comment(e, comment_id)
    if c is None:
        return _bad_response('Comment not found')

    c.delete()

    return _good_response('Comment deleted')

@csrf_exempt
def entry(request, entry_id):
    e = _get_entry(entry_id)
    if e is None:
        return _bad_response('Entry not found')

    if request.method == 'DELETE':
        e.delete()
        return _good_response('Entry deleted')
    elif request.method == 'POST':
        if 'title' in request.REQUEST:
            e.title = request.REQUEST['title']
        if 'desc' in request.REQUEST:
            e.desc = request.REQUEST['desc']

        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            if 'screenshot' in form.cleaned_data:
                e.screenshot = form.cleaned_data['screenshot']

        e.save()

    return _json_response(e.to_dict())

def screenshot(request, entry_id):
    try:
        e = _get_entry(entry_id)
        if e is None:
            return _bad_response('Entry not found')
        fh = open(e.screenshot.path, 'rb')
        return HttpResponse(fh, mimetype="image/jpg")
    except ObjectDoesNotExist:
        return _bad_response('Entry not found')
