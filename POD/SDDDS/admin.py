from django.contrib import admin

from .models import Category, Symptom, Disease, Doctor, HistoryEntry


class SymptomAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['symptom_text','category']}),
    ]
    list_display = ('symptom_text','category')
    list_filter = ['category']
    search_fields = ['symptom_text']

class DiseaseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['disease_name']}),
        ('Симптомы',    {'fields': ['allowing_symptoms','prohibiting_symptoms']})
    ]
    search_fields = ['disease_name']
    list_display = ['disease_name']
    
    
class DoctorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['doctor_name']}),
        ('Классы заболеваний',  {'fields': ['triggering_diseases']}),
        ('Входит в ОМС',  {'fields': ['is_in_MHI']}),
        ('Входит в ДМС',  {'fields': ['is_in_VHI']})
    ]
    search_fields = ['doctor_name', 'triggering_diseases', 'is_in_MHI', 'is_in_VHI']
    list_display = ['doctor_name', 'is_in_MHI', 'is_in_VHI']

admin.site.register(Category)
admin.site.register(Symptom, SymptomAdmin)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(HistoryEntry)
