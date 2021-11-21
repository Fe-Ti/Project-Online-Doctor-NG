from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'sddds'
urlpatterns = [
    # ~ path('index_json/', views.index, name='index_json'),
    # ~ path('odapi/', views.odapi, name='odapi'),
    
    path('', views.index, name='index'),
    path('symptoms/', views.symptoms, name='symptoms'),
    path('process-symptoms/', views.process_symptoms, name='process_symptoms'),
    path('result/', views.results, name='result'),
    path('anonymous-result?<str:doctors>', views.anonymous_result, name='anonymous_result'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
