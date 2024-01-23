from django.urls import path
from accounts import views
from .views import *
from django.conf import settings

from cryptography.fernet import Fernet
from base.crypto import secret_key

f = Fernet(secret_key)

urlpatterns = [
    
    path('logout_user', views.logout_user, name='logout_user'),

    path(f.encrypt(b'73').decode() + '/', views.admind, name='admind'),
    path(f.encrypt(b'74').decode() + '/', views.usercreation, name='usercreation'),
    path(f.encrypt(b'82').decode() + '/', views.createadmin, name='createadmin'),


    path(f.encrypt(b'79').decode() + '/', views.superadmin, name='superadmin'),
    path(f.encrypt(b'80').decode() + '/', views.superadminapi, name='superadmin-api'),
    path(f.encrypt(b'87').decode() +'/<str:pk>/', views.accountdetail, name='accountdetail'),

    path(f.encrypt(b'72').decode() + '/', UserPasswordChangeView.as_view(),name='changepwd'),
    

    path(f.encrypt(b'83').decode() + '/', views.creatregion, name='creatregion'),
    path(f.encrypt(b'92').decode() + '/', views.createpis, name='createpis'),
    path(f.encrypt(b'93').decode() + '/', views.createpiscd, name='createpiscd'),
    path(f.encrypt(b'94').decode() + '/', views.createpr, name='createpr'),

    path(f.encrypt(b'86').decode() + '/', views.admins, name='admins'),
    path(f.encrypt(b'81').decode() + '/', views.superadmins, name='superadmins'),
    path(f.encrypt(b'91').decode() +'/<str:pk>/', views.regions, name='regions'),
    path(f.encrypt(b'99').decode() +'/<str:pk>/', views.case2datas, name='case2data'),
    path(f.encrypt(b'71').decode() +'/<str:pk>/', views.case3datas, name='case3data'),

    path(f.encrypt(b'77').decode() +'/<str:pk>/', views.resetpassword, name='reset'),
    path(f.encrypt(b'78').decode() +'/<str:pk>/', views.deleteuser, name='deleteuser'),
    path(f.encrypt(b'88').decode() +'/<str:pk>/', views.changeadmin, name='changeadmin'),

    path(f.encrypt(b'75').decode() +'/<str:pk>/', views.downloadreasonv, name='downloadreason'),
    path(f.encrypt(b'76').decode() +'/<str:pk>/', views.downloadtm, name='downloadreasontm'),
    
    path(f.encrypt(b'84').decode() + '/', views.downloadveh, name='downloads'),
    path(f.encrypt(b'97').decode() + '/', views.downloadTh, name='downloadedt'),
    path(f.encrypt(b'98').decode() + '/', views.downloadMr, name='downloadedm'),

    
    path(f.encrypt(b'95').decode() +'/<str:pk>/', views.downloaded_detail, name='downloaded_detail'),
    path(f.encrypt(b'96').decode() +'/<str:pk>/', views.downloaded_detail2, name='downloaded_detail2'),
    
    

    path(f.encrypt(b'85').decode() + '/', views.accountlogs, name='logs'),
    path(f.encrypt(b'89').decode() + '/', views.get_apiuser, name='api-user'),
    path(f.encrypt(b'90').decode() +'/<str:pk>/', views.api_activation, name = 'api_activation'),


    path('<str:encoded_id>/', views.decoded_view, name='decoded_view'),

]
