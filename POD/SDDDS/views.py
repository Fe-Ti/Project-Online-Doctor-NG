# Copyright 2021 Fe-Ti <btm.007@mail.ru>
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect 
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.urls import reverse

import json

from . import models

DOCTOR_LIST = 'dlist'
SYMPTOM_LIST = 'slist'

## Error strings
NOT_AUTHENTICATED = 'Пользователь не аутентифицирован. Войдите в аккаунт.'
UNKNOWN_ERROR = 'Неизвестно.'

def to_pk_set(qs):
    pk_set = set()
    for i in list(qs):
        pk_set.add(i.pk)
    return pk_set

def sddprocessor(slist): # SET_OF_ITEMS = ALLOWING_SET - PROHIBITING_SET
    dlist = []
    present_symptoms = []
    allowing_dis_set = set()
    prohibiting_dis_set = set()
    doctor_set = set()
    prohibiting_doc_set = set()
    
    for i in slist:
        recieved = models.Symptom.objects.filter(symptom_text=i)
        if len(recieved) > 0:
            present_symptoms.append(recieved[0].pk)
    for i in present_symptoms: # code style should be improved
        allowing_dis_set |= to_pk_set(models.Disease.objects.filter(
                allowing_symptoms=i) # getting primary keys
        )
        prohibiting_dis_set |= to_pk_set(models.Disease.objects.filter(
                prohibiting_symptoms=i)
        )
    disease_set = allowing_dis_set - prohibiting_dis_set # substracting
    for i in disease_set:
        doctor_set |= to_pk_set(models.Doctor.objects.filter(
                triggering_diseases=i) # getting PK again
        )
    result = list(doctor_set)
    return result

def error(request):
    if not request.user.is_authenticated:
        return render(request, 'SDDDS/error.html', {'type': NOT_AUTHENTICATED})
    return render(request, 'SDDDS/error.html', {'type': UNKNOWN_ERROR})

def index(request):
    return render(request, 'SDDDS/index.html')

def symptoms(request):
    categories = models.Category.objects.all().order_by('category_name')
    return render(request, 'SDDDS/index.html', {'categories':categories})

def process_symptoms(request):
    if request.method == 'POST': # check if the request is POST
        if SYMPTOM_LIST in request.POST:
            result = sddprocessor(request.POST.getlist(SYMPTOM_LIST))
            json_in = json.dumps(request.POST.getlist(SYMPTOM_LIST))
            json_out = json.dumps(result)
            
            if request.user.is_authenticated:
                models.HistoryEntry.objects.create(
                                                    user = request.user,
                                                    symptoms = json_in,
                                                    result = json_out
                                                  )
                return HttpResponseRedirect(reverse('sddds:result'))
            else:
                dstr = ''
                for i in result:
                    dstr = models.Doctor.objects.get(pk=i).doctor_name)+'\n'+dstr
                return HttpResponseRedirect(reverse('sddds:anonymous_result'), dstr)
    return HttpResponseRedirect(reverse('sddds:symptoms'))

def result(request): # Show the most recent history entry
    if request.user.is_authenticated:
        latest_entry = models.HistoryEntry.objects.filter(user=request.user).latest()
        doctor_pks = json.loads(latest_entry.result)
        doctors = list()
        for i in doctor_pks[DOCTOR_LIST]:
            doctors.append(models.Doctor.objects.get(pk=i).doctor_name)
        return render(request, 'SDDDS/results.html', {'doctors':doctors})
    return HttpResponseRedirect(reverse('sddds:error'))

def anonymous_result(request, result):
    doctors = result.split('\n')
    return render(request, 'SDDDS/results.html', {'doctors':doctors})

# Deprecated API
# we'll fallback to it if i screw up in templates
# ~ def get_symptoms():
    # ~ response = dict()
    # ~ cat_list = list(models.Category.objects.all())
    # ~ symp_names = []
    # ~ for i in cat_list:
        # ~ symp_list = list(i.symptom_set.all())
        # ~ for j in symp_list:
            # ~ symp_names.append(j.symptom_text)
        # ~ response[i.category_name] = symp_names[:]
        # ~ symp_names.clear()
    # ~ return response

# ~ def index_json(request):
    # ~ jresponse = get_symptoms()
    # ~ return JsonResponse(jresponse)
    # ~ # returns something like this:
    # ~ # {category:[symptoms], category:[symptoms],...}

# ~ #@ensure_csrf_cookie
# ~ @csrf_exempt # for testing purposes
# ~ def odapi(request):
    # ~ if request.method == 'POST': # check if the request is POST
        # ~ json_in = json.loads(request.readline()) # get the JSON
        # ~ json_out = sddprocessor(json_in[SYMPTOM_LIST], 'external') # process it
        # ~ return JsonResponse(json_out) # response with JSON
    # ~ return HttpResponseBadRequest('No JSON data.') # or say the user to be moron
