from django.core.exceptions import ObjectDoesNotExist
from django.http import \
    HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django import forms
from django.views.decorators.csrf import csrf_exempt
from models import JournalEntry, JournalUser
import json


SUGAR_BUDDY_HEADER = 'HTTP_X_SUGAR_BUDDY'

def _get_user_from_request(request):
    sugar_id = request.META.get(SUGAR_BUDDY_HEADER, None)
    return _get_or_create_user(sugar_id)

def _get_or_create_user(sugar_id):
    u = None
    try:
        u = JournalUser.objects.get(sugar_id=sugar_id)
    except ObjectDoesNotExist:
        u = JournalUser.objects.create(sugar_id=sugar_id)

    return u

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

def _get_entry(user, entry_id):
    try:
        return user.journalentry_set.get(id=entry_id)
    except ObjectDoesNotExist:
        return None

def _get_comment(e, comment_id):
    try:
        return e.comment_set.get(id=comment_id)
    except ObjectDoesNotExist:
        return None

@csrf_exempt
def index(request):
    user = _get_user_from_request(request)

    if request.POST:
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            req_params = request.REQUEST
            screenshot = form.cleaned_data['screenshot']
            e = u.journalentry_set.create(title=req_params['title'],
                                          desc=req_params['desc'],
                                          screenshot=screenshot)
            e.save()
            return _json_response(e.to_dict())
        else:
            return _bad_response('Bad params')
    else:
        entries = [e.to_dict() for e in user.journalentry_set.all()]
        return _json_response(entries)

@csrf_exempt
def comments_index(request, entry_id):
    user = _get_user_from_request(request)
    e = _get_entry(user, entry_id)
    if e is None:
        return _bad_response('Entry not found')

    if request.method == 'POST':
        c = e.comment_set.create(text=request.REQUEST['text'])
        return _json_response(c.to_dict())
    else:
        comments = [c.to_dict() for c in e.comment_set.all()]
        return _json_response(comments)

@csrf_exempt
def comment(request, entry_id, comment_id):
    user = _get_user_from_request(request)

    if request.method != 'DELETE':
        return _bad_response('Bad request')

    e = _get_entry(user, entry_id)
    if e is None:
        return _bad_response('Entry not found')

    c = _get_comment(e, comment_id)
    if c is None:
        return _bad_response('Comment not found')

    c.delete()

    return _good_response('Comment deleted')

@csrf_exempt
def entry(request, entry_id):
    user = _get_user_from_request(request)

    e = _get_entry(user, entry_id)
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
    user = _get_user_from_request(request)

    try:
        e = _get_entry(user, entry_id)
        if e is None:
            return _bad_response('Entry not found')
        fh = open(e.screenshot.path, 'rb')
        return HttpResponse(fh, mimetype="image/jpg")
    except ObjectDoesNotExist:
        return _bad_response('Entry not found')
