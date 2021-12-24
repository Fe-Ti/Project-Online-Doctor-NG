# Copyright 2021 Fe-Ti <btm.007@mail.ru>
import json

from . import models

def to_pk_set(qs):
    pk_set = set()
    for i in list(qs):
        pk_set.add(i.pk)
    return pk_set

def slist_to_pkslist(slist):
    present_symptoms = []
    for i in slist:
        recieved = models.Symptom.objects.filter(symptom_text=i)
        if len(recieved) > 0:
            present_symptoms.append(recieved[0].pk)
    return present_symptoms

def sddprocessor(slist): # SET_OF_ITEMS = ALLOWING_SET - PROHIBITING_SET
    """
    Returns a list of doctors.
    """
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

