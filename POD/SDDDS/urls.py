from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

app_name = 'sddds'
urlpatterns = [
    # ~ path('index_json/', views.index, name='index_json'),
    # ~ path('odapi/', views.odapi, name='odapi'),
    
    path('', views.index, name='index'),
    path('symptoms/', views.symptoms, name='symptoms'),
    path('test/', views.symptoms, name='symptoms'),
    path('process-symptoms/', views.process_symptoms, name='process_symptoms'),
    path('result/', views.results, name='result'),
    path('history/', views.history, name='history'),
    path('anonymous-result/<str:result>', views.anonymous_result, name='anonymous_result'),
    path('registration/form', views.register_form, name='register_form'),
    path('registration/register', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('accounts/profile/', views.accprofile, name='accprofile'),
    path('login/', auth_views.LoginView.as_view(template_name='SDDDS/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='SDDDS/logged_out.html'), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
