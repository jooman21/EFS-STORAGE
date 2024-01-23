import os
from django.core.files import File
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from itertools import chain
from .forms import *
from .models import *
from .serializers import *
from base.crypto import secret_key
from accounts.views import *


from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication  # check me

# from django_elasticsearch_dsl import search
# from elasticsearch_dsl import Q
# from accounts.documents import UserDocument, RegionsDocument
# from base.documents import VehDocument, TMDocument

from cryptography.fernet import Fernet, InvalidToken


f = Fernet(secret_key)


def decoded_view(request, encoded_id):
    try:
        id = f.decrypt(encoded_id.encode()).decode()
        views_mapping = {
            '1': home,
            '2': upload,
            '3': uploadcd,
            '4': case2,
            '5': case3,
            '10': adminsearch-engin,
            '11': detail,
            '12': detail2,
            '13': deleteCase,
            '14': deleteCase2,
            '15': theftevent,
            '16': murderevent,
            '17': deletedevent,
            '18': statics,
            '19': search,
            '20': deleventdetail,
            '21': deleventdetail2,
            '22': deletedevent2,
            '23': deletedevent3,
            '24': deletevent2,
            '25': deletevent,
            '26': adminsearch,
        }
        if id in views_mapping:
            return views_mapping[id](request)
        else:
            raise ValueError("Invalid ID")

    except InvalidToken:
        messages.warning(
            request, 'Your session has expired. Please refresh the page.')
        logout(request)
        return render(request, 'note.html')

    except ValueError as e:
        messages.error(request, str(e))
        return render(request, 'note.html')

# login user --- login.html


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                auth.login(request, user)
                request.session.set_expiry(900)
                # request.session.set_expiry(360)
                return redirect('superadmin')
            elif user.is_staff:
                auth.login(request, user)
                request.session.set_expiry(900)
                # request.session.set_expiry(180)
                return redirect('admind')
            elif user.is_active and user.email == '':
                auth.login(request, user)
                request.session.set_expiry(900)
                # request.session.set_expiry(90)
                return redirect('home')
        # Redirect for all other cases of failed authentication
        messages.info(request, "Invalid Credentials or Unauthorized Access")
        return redirect('login')

    return render(request, 'login.html')


# active user home page     ---     base/home.html
@login_required(login_url='login')
def home(request):
    v_video = VehicleVideo.objects.filter(uploaded_by=request.user)
    TM_video = TheftMurderVideo.objects.filter(uploaded_by=request.user)
    event_views = list(chain(v_video, TM_video))

    paginator = Paginator(event_views, 50)  # 50 items per page
    page = request.GET.get('page', 1)
    event_views = paginator.get_page(page)

    context = {'Eventviews': event_views}
    return render(request, 'base/home.html', context)


# upload vehicle accidents  Local Plate    ---     base/upload.html
@login_required(login_url='login')
def upload(request):
    vidform = VehicleForm()
    if request.method == 'POST':
        vidform = VehicleForm(request.POST, request.FILES)
        if vidform.is_valid():
            video = vidform.cleaned_data['video']
            plate = vidform.cleaned_data['local_plate']
            reg = vidform.cleaned_data['plate_region']
            num = vidform.cleaned_data['plate_number']
            title = str(video).split('_')
            if len(title) == 3:
                VehicleVideo(title=title[0], video=video, created=title[1][0:4] + "-" + title[1][4:6] + "-" + title[1][6:8], incident='Car_Incident',
                             local_plate=plate, plate_region=reg, plate_number=num, uploaded_by=request.user, region=request.user.region).save()
                return redirect('home')
            else:
                messages.error(
                    request, 'Error Occured. File Name Is Not Valid')
        else:
            vidform = VehicleForm()
            messages.error(request, 'Error Occured. Check Your Form')
            return redirect('upload')
    context = {'vidform': vidform}
    return render(request, 'base/upload.html', context)


# upload vehicle accidents  Code Diplomat plate    ---     base/uploadcd.html
@login_required(login_url='login')
def uploadcd(request):
    vidformcd = VehicleFormcd()
    if request.method == 'POST':
        vidformcd = VehicleFormcd(request.POST, request.FILES)
        if vidformcd.is_valid():
            video = vidformcd.cleaned_data['video']
            num = vidformcd.cleaned_data['plate_number']
            plate = vidformcd.cleaned_data['diplomat_plate']
            title = str(video).split('_')
            if len(title) == 3:
                VehicleVideo(title=title[0], video=video, created=title[1][0:4] + "-" + title[1][4:6] + "-" + title[1][6:8],
                             incident='Car_Incident', diplomat_plate=plate, plate_number=num, uploaded_by=request.user, region=request.user.region).save()
                return redirect('home')
            else:
                messages.error(
                    request, 'Error Occured. File Name Is Not Valid')
        else:
            vidformcd = VehicleFormcd()
            messages.error(request, 'Error Occured. Check Your Form')
            return redirect('uploadcd')
    context = {'vidformcd': vidformcd}
    return render(request, 'base/uploadcd.html', context)


# upload Theft         ---     base/case2.html
@login_required(login_url='login')
def case2(request):
    tVform = TheftMurderForm()
    if request.method == 'POST':
        tVform = TheftMurderForm(request.POST, request.FILES)
        if tVform.is_valid():
            video = tVform.cleaned_data['video']
            title = str(video).split('_')
            if len(title) == 3:
                TheftMurderVideo(title=title[0], video=video, created=title[1][0:4] + "-" + title[1][4:6] + "-" +
                                 title[1][6:8], incident='Theft', uploaded_by=request.user, region=request.user.region).save()
                return redirect('home')
            else:
                messages.error(
                    request, 'Error Occured. File Name Is Not Valid')
        else:
            tVform = TheftMurderForm()
            messages.error(request, 'Error Occured. Check Your Form')
            return redirect('case2')
    context = {'tVform': tVform}
    return render(request, 'base/case2.html', context)


# upload Murder cases        ---     base/case3.html
@login_required(login_url='login')
def case3(request):
    mVform = TheftMurderForm()
    if request.method == 'POST':
        mVform = TheftMurderForm(request.POST, request.FILES)
        if mVform.is_valid():
            video = mVform.cleaned_data['video']
            title = str(video).split('_')
            if len(title) == 3:
                TheftMurderVideo(title=title[0], video=video, created=title[1][0:4] + "-" + title[1][4:6] + "-" +
                                 title[1][6:8], incident='Murder', uploaded_by=request.user, region=request.user.region).save()
                return redirect('home')
            else:
                messages.error(
                    request, 'Error Occured. File Name Is Not Valid')

        else:
            mVform = TheftMurderForm()
            messages.error(request, 'Error Occured. Check Your Form')
            return redirect('case3')
    context = {'mVform':  mVform}
    return render(request, 'base/case3.html', context)



@login_required(login_url='login')
def deleteCase(request, pk):
    videos = VehicleVideo.objects.get(id=pk)
    deleted = DeletedVehicle()
    form = dvehForm()  # Use the updated form with validation logic
    downloadedveh = DownloadedVehicle.objects.filter(video=videos)

    if request.method == 'POST':
        form = dvehForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']

            deleted.video = File(
                videos.video, os.path.basename(videos.video.path))

            if videos.local_plate is not None:
                if downloadedveh.exists():
                    downloadvehnum = downloadedveh.count()
                    DeletedVehicle(title=videos.title, video=deleted.video, uploaded_by=videos.uploaded_by, created=videos.created, upload=videos.upload.date(), incident=videos.incident, local_plate=videos.local_plate,
                                   plate_region=videos.plate_region, plate_number=videos.plate_number, region=request.user.region, deleted_by=request.user, reason=reason, number_of_download=downloadvehnum).save()
                else:
                    DeletedVehicle(title=videos.title, video=deleted.video, uploaded_by=videos.uploaded_by, created=videos.created, upload=videos.upload.date(), incident=videos.incident, local_plate=videos.local_plate,
                                   plate_region=videos.plate_region, plate_number=videos.plate_number, region=request.user.region, deleted_by=request.user, reason=reason, number_of_download='0').save()
            else:
                if downloadedveh.exists():
                    downloadvehnum = downloadedveh.count()
                    DeletedVehicle(title=videos.title, video=deleted.video, uploaded_by=videos.uploaded_by, created=videos.created, upload=videos.upload.date(), incident=videos.incident,
                                   diplomat_plate=videos.diplomat_plate, plate_number=videos.plate_number, region=request.user.region, deleted_by=request.user, reason=reason, number_of_download=downloadvehnum).save()
                else:
                    DeletedVehicle(title=videos.title, video=deleted.video, uploaded_by=videos.uploaded_by, created=videos.created, upload=videos.upload.date(), incident=videos.incident,
                                   diplomat_plate=videos.diplomat_plate, plate_number=videos.plate_number, region=request.user.region, deleted_by=request.user, reason=reason, number_of_download='0').save()

            videos.video.close()
            videos.clean()
            videos.delete()
            
            if request.user.is_superuser:
                return redirect('superadmin')
            else:
                return redirect('admind')
        else:
            messages.error(request, 'Please provide a valid and meaningful reason (minimum 10 characters).')
            context = {'video': videos, 'form': form, }
            return render(request, 'base/deleteCase.html', context)

    context = {'video': videos, 'form': form}
    return render(request, 'base/deleteCase.html', context)


@login_required(login_url='login')
def deleteCase2(request, pk):
    videos = TheftMurderVideo.objects.get(id=pk)
    deleted = DeletedTM()
    form = dTMForm()
    downloadedTM = DownloadedTM.objects.filter(video=videos)
    if request.method == 'POST':
        form = dTMForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']

            deleted.video = File(
                videos.video, os.path.basename(videos.video.path))
            if downloadedTM.exists():
                downloadTMnum = downloadedTM.count()
                DeletedTM(title=videos.title, video=deleted.video, uploaded_by=videos.uploaded_by, created=videos.created, upload=videos.upload.date(
                ), incident=videos.incident, region=request.user.region, deleted_by=request.user, reason=reason, number_of_download=downloadTMnum).save()
            else:
                DeletedTM(title=videos.title, video=deleted.video, uploaded_by=videos.uploaded_by, created=videos.created, upload=videos.upload.date(
                ), incident=videos.incident, region=request.user.region, deleted_by=request.user, reason=reason, number_of_download='0').save()

        videos.video.close()
        videos.clean()
        videos.delete()
        if request.user.is_superuser:
            return redirect('superadmin')
        else:
            return redirect('admind')
    context = {'video': videos, 'form': form}
    return render(request, 'base/deleteCase2.html', context)


# vehicle Video Details     ---     base/detail.html
@login_required(login_url='login')
def vehdetail(request, pk):
    videos = VehicleVideo.objects.get(id=pk)
    context = {'videos': videos}
    return render(request, 'base/detail.html', context)


# theft and Murder Video Detail ---     base/detail2.html
@login_required(login_url='login')
def TMdetail(request, pk):
    TMvideos = TheftMurderVideo.objects.get(id=pk)
    context = {'TMvideos': TMvideos}
    return render(request, 'base/detail2.html', context)


# super-user statics page       ---     base/statics.html
@login_required(login_url='login')
def statics(request):
    regions = Regions.objects.all()
    total_regions = regions.count()
    total_vehicle = VehicleVideo.objects.all().count()
    total_murder = TheftMurderVideo.objects.filter(incident="Murder").count()
    total_theft = TheftMurderVideo.objects.filter(incident="Theft").count()
    total_Events = total_vehicle + total_murder + total_theft

    total_veh_download = DownloadedVehicle.objects.all().count()
    total_the_download = DownloadedTM.objects.filter(incident="Theft").count()
    total_mur_download = DownloadedTM.objects.filter(incident="Murder").count()

    adminaccounts = User.objects.filter(
        is_staff=True, is_superuser=False).count()
    useraccounts = User.objects.filter(is_staff=False, is_active=True).count()
    Super_account = User.objects.filter(
        is_superuser=True, is_staff=True, is_active=True).count()
    api_users = User.objects.filter(email__gt='', email__isnull=False).count()

    del_veh = DeletedVehicle.objects.all().count()
    del_TM = DeletedTM.objects.all().count()
    total_del_vid = del_TM + del_veh

    context = {'total_regions': total_regions, 'adminaccounts': adminaccounts, 'useraccounts': useraccounts,
               'total_theft': total_theft, 'total_murder': total_murder, 'total_vehicle': total_vehicle, 'total_Events': total_Events, 'Super_accounts': Super_account, 'api_users': api_users,
               'total_veh_download': total_veh_download, 'total_the_download': total_the_download, 'total_mur_download': total_mur_download, 'total_del_vid': total_del_vid
               }
    return render(request, 'base/statics.html', context)


# Elasticsearch
# Elasticsearch For  staff users (regional admins)    ---     base/adminsearch-engin.html
@login_required(login_url='login')
def adminsearchengin(request):
    q = request.GET.get('q')
    d = request.GET.get('d')

    results = []
    if q and d:
        search_query = Q('multi_match', query=q, fields=[
                         'title', 'incident', 'plate_number', 'plate_region', 'diplomat_plate'])
        date_query = Q('match', created=d)

        total_query = search_query & date_query

        vehicle_search = VehDocument.search().query(total_query)
        theftmurder_search = TMDocument.search().query(total_query)

        vehicle_results = vehicle_search.execute()
        theftmurder_results = theftmurder_search.execute()

        vehicle_ids = [hit.meta.id for hit in vehicle_results.hits]
        theftmurder_ids = [hit.meta.id for hit in theftmurder_results.hits]

        vehicle_objects = [VehicleVideo.objects.get(pk=id) for id in vehicle_ids if VehicleVideo.objects.get(
            pk=id).uploaded_by.admin_name == request.user.username]

        theftmurder_objects = [TheftMurderVideo.objects.get(pk=id) for id in theftmurder_ids if TheftMurderVideo.objects.get(
            pk=id).uploaded_by.admin_name == request.user.username]

        results = vehicle_objects + theftmurder_objects

    context = {'v_video': results}
    return render(request, 'base/adminsearch-engin.html', context)


# Elasticsearch
# super-user search results page     ---     base/adminsearch.html
@login_required(login_url='login')
def adminsearch(request):
    q = request.GET.get('q')
    d = request.GET.get('d')

    results = []
    if q and d:
        search_query = Q('multi_match', query=q, fields=[
                         'title', 'incident', 'plate_number', 'plate_region', 'diplomat_plate'])
        date_query = Q('match', created=d)

        total_query = search_query & date_query

        vehicle_search = VehDocument.search().query(total_query)
        theftmurder_search = TMDocument.search().query(total_query)

        vehicle_results = vehicle_search.execute()
        theftmurder_results = theftmurder_search.execute()

        vehicle_ids = [hit.meta.id for hit in vehicle_results.hits]
        theftmurder_ids = [hit.meta.id for hit in theftmurder_results.hits]

        vehicle_objects = [VehicleVideo.objects.get(
            pk=id) for id in vehicle_ids]
        theftmurder_objects = [TheftMurderVideo.objects.get(
            pk=id) for id in theftmurder_ids]

        results = vehicle_objects + theftmurder_objects

    context = {'v_video': results}
    return render(request, 'base/adminsearch.html', context)


# admins-deleted event search page------------------------------------
@login_required(login_url='login')
def search(request):
    q = request.GET.get('q')
    d = request.GET.get('d')

    if DeletedVehicle.objects.exists() and DeletedTM.objects.exists():

        if d != None:
            delveh = DeletedVehicle.objects.filter(
                Q(title__icontains=q) & Q(upload__icontains=d))
            deltm = DeletedTM.objects.filter(
                Q(title__icontains=q) & Q(upload__icontains=d))
        else:
            messages.info(request, "No Input's")
    else:
        delveh = DeletedVehicle.objects.all()
        deltm = DeletedTM.objects.all()
        messages.info(request, "Empty Database")

    DeletedEvent = chain(delveh, deltm)
    context = {"v_video": DeletedEvent}
    return render(request, 'base/search.html', context)


# Admin list of theft events    ---   base/murderevent.html
@login_required(login_url='login')
def murderevent(request):

    # TheftMurderVideo incidents       Murder
    murvid = TheftMurderVideo.objects.filter(incident='Murder')

    # Count of employees for the admin user
    employees_admin = User.objects.filter(
        admin_name=request.user.username).count()

    # VehicleVideo related counts
    vehvid = VehicleVideo.objects.all()
    total_vehvid = vehvid.count()

    total_users_post_v = [
        users_post.uploaded_by.admin_name for users_post in VehicleVideo.objects.all()]
    number_of_posts_v = [
        x for x in total_users_post_v if request.user.username == x]
    counted_v = len(number_of_posts_v)

    # TheftMurderVideo related counts for Murder incidents
    total_users_post_M = [
        users_post.uploaded_by.admin_name for users_post in TheftMurderVideo.objects.filter(incident='Murder')]
    number_of_posts_m = [
        x for x in total_users_post_M if request.user.username == x]
    counted_m = len(number_of_posts_m)

    # TheftMurderVideo related counts for Theft incidents
    total_users_post_T = [
        users_post.uploaded_by.admin_name for users_post in TheftMurderVideo.objects.filter(incident='Theft')]
    number_of_posts_t = [
        x for x in total_users_post_T if request.user.username == x]
    counted_t = len(number_of_posts_t)

    # Total count per admin for all incidents
    total_per_admin = counted_v + counted_m + counted_t

    # pagination
    mud = TheftMurderVideo.objects.filter(
        incident='Murder', region=request.user.region).order_by('id')
    p = Paginator(mud, 20)
    page = request.GET.get('page')
    murder_list = p.get_page(page)

    context = {'employees_admin': employees_admin, 'murvid': murvid, 'total_vehvid': total_vehvid, 'counted_v': counted_v, 'counted_m': counted_m,
               'counted_t': counted_t, 'total_per_admin': total_per_admin, 'murder_list': murder_list
               }

    return render(request, 'base/murderevent.html', context)


# Admin list of theft events    ---   base/theftevent.html
@login_required(login_url='login')
def theftevent(request):

    # TheftMurderVideo incidents       Theft
    thfvid = TheftMurderVideo.objects.filter(incident='Theft')

    # Count of employees for the admin user
    employees_admin = User.objects.filter(
        admin_name=request.user.username).count()

    # VehicleVideo related counts
    vehvid = VehicleVideo.objects.all()
    total_vehvid = vehvid.count()

    total_users_post_v = [
        users_post.uploaded_by.admin_name for users_post in VehicleVideo.objects.all()]
    number_of_posts_v = [
        x for x in total_users_post_v if request.user.username == x]
    counted_v = len(number_of_posts_v)

    # TheftMurderVideo related counts for Murder incidents
    total_users_post_M = [
        users_post.uploaded_by.admin_name for users_post in TheftMurderVideo.objects.filter(incident='Murder')]
    number_of_posts_m = [
        x for x in total_users_post_M if request.user.username == x]
    counted_m = len(number_of_posts_m)

    # TheftMurderVideo related counts for Theft incidents
    total_users_post_T = [
        users_post.uploaded_by.admin_name for users_post in TheftMurderVideo.objects.filter(incident='Theft')]
    number_of_posts_t = [
        x for x in total_users_post_T if request.user.username == x]
    counted_t = len(number_of_posts_t)

    # Total count per admin for all incidents
    total_per_admin = counted_v + counted_m + counted_t

    # Pagination for TheftMurderVideo with incident='Theft' and region=request.user.region
    tft = TheftMurderVideo.objects.filter(
        incident='Theft', region=request.user.region).order_by('id')
    p = Paginator(tft, 20)
    page = request.GET.get('page')
    theft_list = p.get_page(page)

    context = {'employees_admin': employees_admin, 'thfvid': thfvid, 'total_vehvid': total_vehvid, 'counted_v': counted_v, 'counted_m': counted_m, 'counted_t': counted_t, 'total_per_admin': total_per_admin, 'theft_list': theft_list
               }
    return render(request, 'base/theftevent.html', context)


@login_required(login_url='login')
def deletedevents(request):
    dveh = DeletedVehicle.objects.all().order_by('id')
    deleted_veichle = DeletedVehicle.objects.filter(
        incident="Car_Incident").count()
    deleted_murder = DeletedTM.objects.filter(incident="Murder").count()
    deleted_theft = DeletedTM.objects.filter(incident="Theft").count()
    total_event = deleted_theft + deleted_murder + deleted_veichle

    p = Paginator(dveh, 50)
    page = request.GET.get('page')
    del_veh_list = p.get_page(page)
    context = {'dveh': dveh, 'deleted_veichle': deleted_veichle, 'deleted_murder': deleted_murder,
               'deleted_theft': deleted_theft, 'total_event': total_event, 'del_veh_list': del_veh_list}
    return render(request, 'base/deletedevent.html', context)


@login_required(login_url='login')
def deletedevents2(request):
    dthe = DeletedTM.objects.filter(incident="Theft").order_by('id')
    deleted_veichle = DeletedVehicle.objects.filter(
        incident="Car_Incident").count()
    deleted_murder = DeletedTM.objects.filter(incident="Murder").count()
    deleted_theft = DeletedTM.objects.filter(incident="Theft").count()
    total_event = deleted_theft + deleted_murder + deleted_veichle

    p = Paginator(dthe, 50)
    page = request.GET.get('page')
    dthe_list = p.get_page(page)

    context = {'deleted_veichle': deleted_veichle, 'deleted_murder': deleted_murder, 'dthe': dthe,
               'deleted_theft': deleted_theft,  'total_event': total_event, 'dthe_list': dthe_list}
    return render(request, 'base/deletedevent2.html', context)


@login_required(login_url='login')
def deletedevents3(request):
    dmur = DeletedTM.objects.filter(incident="Murder").order_by('id')
    deleted_veichle = DeletedVehicle.objects.filter(
        incident="Car_Incident").count()
    deleted_murder = DeletedTM.objects.filter(incident="Murder").count()
    deleted_theft = DeletedTM.objects.filter(incident="Theft").count()
    total_event = deleted_theft + deleted_murder + deleted_veichle

    p = Paginator(dmur, 50)
    page = request.GET.get('page')
    dmur_list = p.get_page(page)

    context = {'deleted_murder': deleted_murder, 'dmur': dmur, 'deleted_veichle': deleted_veichle,
               'deleted_theft': deleted_theft, 'total_event': total_event, 'dmur_list': dmur_list}
    return render(request, 'base/deletedevent3.html', context)


@login_required(login_url='login')
def devent(request, pk):
    video = DeletedVehicle.objects.get(id=pk)
    context = {'video': video}
    return render(request, 'base/deleventdetail.html', context)


@login_required(login_url='login')
def devent2(request, pk):
    video = DeletedTM.objects.get(id=pk)
    context = {'video': video}
    return render(request, 'base/deleventdetail2.html', context)


@login_required(login_url='login')
def erasevent(request, pk):
    video = DeletedVehicle.objects.get(id=pk)
    if request.method == 'POST':
        video.delete()
        if request.user.is_superuser:
            return redirect('superadmin')
    context = {'video': video}
    return render(request, 'base/deletevent.html', context)


@login_required(login_url='login')
def erasevent2(request, pk):
    video = DeletedTM.objects.get(id=pk)
    if request.method == 'POST':
        video.delete()
        if request.user.is_superuser:
            return redirect('superadmin')
    context = {'video': video}
    return render(request, 'base/deletevent2.html', context)


# Api section ------------------------------------------------------------------------------>
@api_view(['GET'])
def Vehicleapi(request):
    vehicle = VehicleVideo.objects.all()
    serializer = VehicleVideoSerializer(vehicle, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Vehicledetail(request, pk):
    vehicle = VehicleVideo.objects.get(id=pk)
    serializer = VehicleVideoSerializer(vehicle, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def TMapi(request):
    vehicle = TheftMurderVideo.objects.all()
    serializer = TheftMurderVideoSerializer(vehicle, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TMapidetail(request, pk):
    vehicle = TheftMurderVideo.objects.get(id=pk)
    serializer = TheftMurderVideoSerializer(vehicle, many=False)
    return Response(serializer.data)


# deleted videos ------------------------------
@api_view(['GET'])
def Vdelapi(request):
    vehicle = DeletedVehicle.objects.all()
    serializer = DeletedVehicleSerializer(vehicle, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Vdelapidetail(request, pk):
    vehicle = DeletedVehicle.objects.get(id=pk)
    serializer = DeletedVehicleSerializer(vehicle, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def TMdelapi(request):
    vehicle = DeletedTM.objects.all()
    serializer = DeletedTMSerializer(vehicle, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TMdelapidetail(request, pk):
    vehicle = DeletedTM.objects.get(id=pk)
    serializer = DeletedTMSerializer(vehicle, many=False)
    return Response(serializer.data)


# downloaded videos --------------------------
@api_view(['GET'])
def Vdowapi(request):
    vehicle = DownloadedVehicle.objects.all()
    serializer = DownloadedVehicleSerializer(vehicle, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Vdowapidetail(request, pk):
    vehicle = DownloadedVehicle.objects.get(id=pk)
    serializer = DownloadedVehicleSerializer(vehicle, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def TMdowapi(request):
    vehicle = DownloadedTM.objects.all()
    serializer = DownloadedTMSerializer(vehicle, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TMdowapidetail(request, pk):
    vehicle = DownloadedTM.objects.get(id=pk)
    serializer = DownloadedTMSerializer(vehicle, many=False)
    return Response(serializer.data)
