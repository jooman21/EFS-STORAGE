from django.urls import path, include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

from cryptography.fernet import Fernet
from base.crypto import secret_key

f = Fernet(secret_key)

urlpatterns = [
    # api url
    path('Vehicle-Event/', Vehicleapi, name='Vehicle-Event'),
    path('Vehicle-detail/<str:pk>/', views.Vehicledetail, name='Vehicle-detail'),
    path('TM-Event/', views.TMapi, name='TM-Event'),
    path('TM-Event/<str:pk>/', views.TMapidetail, name='TM-Event-detail'),

    path('Vdel-Event/', views.Vdelapi, name='Vdel-Event'),
    path('Vdel-detail/<str:pk>/', views.Vdelapidetail, name='Vdel-detail'),
    path('TMdel-Event/', views.TMdelapi, name='TMdel-Event'),
    path('TMdel-detail/<str:pk>/', views.TMdelapidetail, name='TMdel-detail'),

    path('Vdow-Event/', views.Vdowapi, name='Vdow-Event'),
    path('Vdow-detail/<str:pk>/', views.Vdowapidetail, name='Vdow-detail'),
    path('TMdow-Event/', views.TMdowapi, name='TMdow-Event'),
    path('TMdow-detail/<str:pk>/', views.TMdowapidetail, name='TMdow-detail'),



    path('', views.login, name='login'),


    path(f.encrypt(b'1').decode() + '/', views.home, name='home'),
    path(f.encrypt(b'2').decode() + '/', views.upload, name='upload'),
    path(f.encrypt(b'3').decode() + '/', views.uploadcd, name='uploadcd'),
    path(f.encrypt(b'4').decode() + '/', views.case2, name='case2'),
    path(f.encrypt(b'5').decode() + '/', views.case3, name='case3'),

    path(f.encrypt(b'11').decode() +'/<str:pk>/', views.vehdetail, name='vehdetail'),
    path(f.encrypt(b'12').decode() +'/<str:pk>/', views.TMdetail, name='TMdetail'),
    path(f.encrypt(b'13').decode() +'/<str:pk>/', views.deleteCase, name='deleteCase'),
    path(f.encrypt(b'14').decode() +'/<str:pk>/', views.deleteCase2, name='deleteCase2'),

    path(f.encrypt(b'18').decode() +'/', views.statics, name='statics'),


    path(f.encrypt(b'26').decode() + '/', views.adminsearch, name='adminsearch'), 
    path(f.encrypt(b'10').decode() + '/', views.adminsearchengin, name='adminsearch-engin'),
    path(f.encrypt(b'19').decode() + '/', views.search, name='search'),


    path(f.encrypt(b'16').decode() +'/', views.murderevent, name='murderevent'),
    path(f.encrypt(b'15').decode() +'/', views.theftevent, name='theftevent'),

    path(f.encrypt(b'17').decode() +'/', views.deletedevents, name='deletedevent'),
    path(f.encrypt(b'22').decode() +'/', views.deletedevents2, name='deletedevent2'),
    path(f.encrypt(b'23').decode() +'/', views.deletedevents3, name='deletedevent3'),

    path(f.encrypt(b'20').decode() +'/<str:pk>/', views.devent, name='deleventdetail'),
    path(f.encrypt(b'21').decode() +'/<str:pk>/', views.devent2, name='deleventdetail2'),
    path(f.encrypt(b'25').decode() +'/<str:pk>/', views.erasevent, name='deletevent'),
    path(f.encrypt(b'24').decode() +'/<str:pk>/', views.erasevent2, name='deletevent2'),



    path('<str:encoded_id>/', views.decoded_view, name='decoded_view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
