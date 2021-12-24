# Copyright 2021 Fe-Ti <btm.007@mail.ru>
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect 
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

import json

from . import models
from .sddprocessor_lib import to_pk_set, sddprocessor

DOCTOR_LIST = 'dlist'
SYMPTOM_LIST = 'slist'

## Error strings
NOT_AUTHENTICATED = 'Пользователь не аутентифицирован. Войдите в аккаунт.'
UNKNOWN_ERROR = 'Неизвестно.'
REGISTRATION_ERROR = "Ошибка при регистрации"

def index(request):
    return render(request, 'SDDDS/index.html')

def error(request):
    if not request.user.is_authenticated:
        return render(request, 'SDDDS/error_page.html', {'error': NOT_AUTHENTICATED})
    return render(request, 'SDDDS/error_page.html', {'error': UNKNOWN_ERROR})

def symptoms(request):
    categories = models.Category.objects.all().order_by('category_name')
    return render(request, 'SDDDS/symptoms_form.html', {'categories':categories})

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
                    dstr += models.Doctor.objects.get(pk=i).doctor_name + '=='
                return HttpResponseRedirect(reverse('sddds:anonymous_result', args=[dstr[:-2],]))
    return HttpResponseRedirect(reverse('sddds:symptoms'))


def results(request): # Show the most recent history entry
    if request.user.is_authenticated:
        latest_entry = models.HistoryEntry.objects.filter(user=request.user).latest()
        doctor_pks = json.loads(latest_entry.result)
        doctors = list()
        for i in doctor_pks:
            doctors.append(models.Doctor.objects.get(pk=i).doctor_name)
        return render(request, 'SDDDS/results.html', {'doctors':doctors})
    return HttpResponseRedirect(reverse('sddds:error'))

def anonymous_result(request, result):
    doctors = result.split('==')
    return render(request, 'SDDDS/results.html', {'doctors':doctors})

def history(request):
    if request.user.is_authenticated:
        entries = models.HistoryEntry.objects.filter(user=request.user)
        return render(request, 'SDDDS/history.html', {'entries':entries})
    else:
        return HttpResponseRedirect(reverse('sddds:login'))

def profile(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('sddds:history')) #render(request, 'SDDDS/profile.html', {'chats':chats})
    else:
        return HttpResponseRedirect(reverse('sddds:login'))

def accprofile(request):
    return HttpResponseRedirect(reverse('sddds:profile'))

def register_form(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('sddds:profile'))
    else:
        return render(request, 'SDDDS/register_form.html', {'form': AuthenticationForm})

def register(request):
    if not request.user.is_authenticated:
        uname = request.POST.dict()['username']
        passwd = request.POST.dict()['password']
        new_user = User.objects.create_user(username=uname, password=passwd)
        user = authenticate(request, username=uname, password=passwd)
        if user is not None:
            login(request, user)
        else:
            return render(request, 'SDDDS/error_page.html', {'error':REGISTRATION_ERROR})
    
    return HttpResponseRedirect(reverse('sddds:profile'))
