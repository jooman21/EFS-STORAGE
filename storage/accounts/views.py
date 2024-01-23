import os
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import auth
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from .forms import CreateUserForm, createAdminForm, CreateRegionForm, useraccountForm, passwordeditform, superusercreationForm
from .models import *
from base.models import VehicleVideo, TheftMurderVideo, DownloadedVehicle, DownloadedTM, VehiclePlateLocal, VehicleRegion, VehiclePlateCD
from base.forms import downloadVForm, downloadTMForm
from base.crypto import secret_key
from itertools import chain
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
# from .validators import  *
from .validators import UppercaseValidator, LowercaseValidator, SymbolValidator, MinimumLengthValidator
# cryptography
from cryptography.fernet import Fernet, InvalidToken

# rest_framework
from rest_framework.authtoken.models import Token

# Elasticsearch
# from accounts.documents import UserDocument, RegionsDocument
# from django_elasticsearch_dsl import search
# from elasticsearch_dsl import Q
# from base.documents import VehDocument, TMDocument


User = get_user_model()


f = Fernet(secret_key)


def decoded_view(request, encoded_id):
    try:
        id = f.decrypt(encoded_id.encode()).decode()
        views_mapping = {
            '72': changepwd,
            '73': admind,
            '74': usercreation,
            '75': downloadreason,
            '76': downloadreasontm,
            '77': reset,
            '78': deleteuser,
            '79': superadmin,
            '80': superadmin-api,
            '81': superadmins,
            '82': createadmin,
            '83': creatregion,
            '84': downloads,
            '85': logs,
            '86': admins,
            '87': accountdetail,
            '88': changeadmin,
            '89': api-user,
            '90': api_activation,
            '91': regions,
            '92': createpis,
            '93': createpiscd,
            '94': createpr,
            '95': downloaded_detail,
            '96': downloaded_detail2,
            '97': downloadedt,
            '98': downloadedm,
            '99': case2data,
            '71': case3data,
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


# logout user
@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


# create user account only active by the regional admins        ---     accounts/usercreation.html
@login_required(login_url='login')
def usercreation(request):
    newuser = CreateUserForm()
    user_region = User.objects.filter(region=request.user.region)
    users_region = user_region.count()
    standard_user_admin = User.objects.filter(
        admin_name=request.user.username, is_staff=False)

    Total_standard_user = []
    for user in standard_user_admin:
        if user.is_active == True:
            Total_standard_user.append(user)

    number_of_users = len(Total_standard_user)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        region = request.user.region
        admin_name = request.user.username


        if password != password_confirm:
            messages.error(request, 'Password and password confirmation do not match.')
            return redirect('usercreation')
        
         # Custom password validators
        uppercase_validator = UppercaseValidator()
        lowercase_validator = LowercaseValidator()
        symbol_validator = SymbolValidator()
        length_validator = MinimumLengthValidator(min_length=8)
        # Validate password using custom validators
        try:
            uppercase_validator.validate(password)
            lowercase_validator.validate(password)
            symbol_validator.validate(password)
            length_validator.validate(password)
        except ValidationError as e:
            messages.error(request, '\n'.join(e.messages))
            return redirect('usercreation')
        
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            
            if user.is_active == False:
                messages.info(request, 'Blocked Account.')
            else:
                messages.info(request, 'User Already Exists !!')
            return redirect('usercreation')
        else:
            user = User.objects.create_user(username=username, password=password,
                                            first_name=first_name, last_name=last_name, region=region, admin_name=admin_name)
            user.save()
            messages.info(request, 'Account Created !!')
            return redirect('usercreation')

    user_pag = User.objects.filter(
        admin_name=request.user.username, is_staff=False, is_active=True).order_by('id')
    p = Paginator(user_pag, 20)
    page = request.GET.get('page')
    User_list = p.get_page(page)

    context = {'newuser': newuser, 'user_region': user_region, 'users_region': users_region, 'Total_standard_user': Total_standard_user, 'number_of_users': number_of_users, 'User_list': User_list
               }
    return render(request, 'accounts/usercreation.html', context)


# Super-user Create Regional Admins     ---     accounts/createadmin.html
@login_required(login_url='login')
def createadmin(request):
    newadmin = createAdminForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        regionid = request.POST.get('region')
        
        if password != password_confirm:
            messages.error(request, 'Password and password confirmation do not match.')
            return redirect('createadmin')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'USERNAME ALREADY EXISTS !!')
            return redirect('createadmin')
        uppercase_validator = UppercaseValidator()
        lowercase_validator = LowercaseValidator()
        symbol_validator = SymbolValidator()
        length_validator = MinimumLengthValidator(min_length=8)
        # Validate password using custom validators
        try:
            uppercase_validator.validate(password)
            lowercase_validator.validate(password)
            symbol_validator.validate(password)
            length_validator.validate(password)
        except ValidationError as e:
            messages.error(request, '\n'.join(e.messages))
            return redirect('usercreation')
        else:
            try:
                region = Regions.objects.get(id=regionid)
                User.objects.create_user(username=username, password=password, first_name=first_name,
                                         last_name=last_name, is_staff=True, admin_name=username, region=region).save()
                return redirect('admins')
            except Regions.DoesNotExist:
                messages.error(request, 'Region does not exist.')
                return redirect('createadmin')
    context = {'newadmin': newadmin}
    return render(request, 'accounts/createadmin.html', context)


# Super-user Total Admin Account's Page    ---     accounts/admins.html
@login_required(login_url='login')
def admins(request):
    admins = User.objects.filter(
        is_superuser=False, is_staff=True, is_active=True).order_by('id')
    total_admins = admins.count()

    p = Paginator(admins, 10)
    page = request.GET.get('page')
    adm_reg_list = p.get_page(page)

    context = {'admins': admins, 'total_admins': total_admins,
               'adm_reg_list': adm_reg_list}
    return render(request, 'accounts/admins.html', context)


# Super-user Total Super admin Accounts        ---      accounts/superadmins.html
@login_required(login_url='login')
def superadmins(request):
    superuser = User.objects.filter(
        is_superuser=True, is_staff=True, is_active=True)
    total_superuser = superuser.count()

    context = {'superuser': superuser, 'total_superuser': total_superuser}
    return render(request, 'accounts/superadmins.html', context)


# super-user super-admin Create Region Page    --- accounts/creatregion.html
@login_required(login_url='login')
def creatregion(request):
    regionform = CreateRegionForm()
    regionnum = Regions.objects.all().count()
    if request.method == 'POST':
        region = request.POST.get('name')
        if Regions.objects.filter(name=region).exists():
            messages.info(request, 'Region Exists !')
        else:
            Regions(name=region, created_by=request.user).save()
            messages.success(request, 'Region Created')

    ordered_regions = Regions.objects.order_by('id')
    p = Paginator(ordered_regions, 10)
    page = request.GET.get('page')
    Region_list = p.get_page(page)
    context = {'regionform': regionform,
               'Region_list': Region_list, 'regionnum': regionnum}
    return render(request, 'accounts/creatregion.html', context)


# super-user create Local Plate intended service       ---      accounts/createpis.html
@login_required(login_url='login')
def createpis(request):
    plateservice = VehiclePlateLocal.objects.all().count()
    if request.method == 'POST':
        pis_id = request.POST.get('num')
        pis = request.POST.get('pis')

        if VehiclePlateLocal.objects.filter(plate_id=pis_id).exists():
            messages.info(request, 'Intended Service Number Exists!!')
        elif VehiclePlateLocal.objects.filter(plate_name=pis).exists():
            messages.info(request, 'Intended Service Name Exists !!')
        else:
            VehiclePlateLocal(plate_id=pis_id, plate_name=pis,
                              created_by=request.user).save()
            messages.success(request, 'Plate Condition Created')

    veh = VehiclePlateLocal.objects.all().order_by('id')
    p = Paginator(veh, 10)
    page = request.GET.get('page')
    Pis_list = p.get_page(page)
    context = {'plateservice': plateservice, 'Pis_list': Pis_list}
    return render(request, 'accounts/createpis.html', context)


# super-user create Code Diplomat plate service number     ---     accounts/createpiscd.html
@login_required(login_url='login')
def createpiscd(request):
    plateservice = VehiclePlateCD.objects.all().count
    if request.method == 'POST':
        pis_id = request.POST.get('num')
        pis = request.POST.get('pis')
        if VehiclePlateCD.objects.filter(plate_id=pis_id).exists():
            messages.info(request, 'Intended Service Number Exists !!')
        elif VehiclePlateCD.objects.filter(plate_name=pis).exists():
            messages.info(request, 'Intended Service Name Exists !!')
        else:
            VehiclePlateCD(plate_id=pis_id, plate_name=pis,
                           created_by=request.user).save()
            messages.success(request, 'Plate Condition Created')

    veh = VehiclePlateCD.objects.all().order_by('id')
    p = Paginator(veh, 10)
    page = request.GET.get('page')
    Pis_list = p.get_page(page)
    context = {'plateservice': plateservice, 'Pis_list': Pis_list}
    return render(request, 'accounts/createpiscd.html', context)


# super-user create Plate regions      ---     accounts/createpr.html
@login_required(login_url='login')
def createpr(request):
    plateregion = VehicleRegion.objects.all().count
    if request.method == 'POST':
        pis = request.POST.get('pis')
        if VehicleRegion.objects.filter(region_name=pis).exists():
            messages.info(request, 'Plate Region Exists !!')
        else:
            VehicleRegion(region_name=pis, created_by=request.user).save()
            messages.success(request, 'Plate Region Created')
    veh = VehicleRegion.objects.all().order_by('id')
    p = Paginator(veh, 10)
    page = request.GET.get('page')
    Preg_list = p.get_page(page)
    context = {'plateregion': plateregion, 'Preg_list': Preg_list}
    return render(request, 'accounts/createpr.html', context)


# regional admin Page       ---     accounts/admind.html
@login_required(login_url='login')
def admind(request):
    user_admin_name = request.user.username
    total_vehvid = VehicleVideo.objects.count()

    # Total counts for Murder and Theft incidents
    total_murvid = TheftMurderVideo.objects.filter(incident='Murder').count()
    total_thfvid = TheftMurderVideo.objects.filter(incident='Theft').count()

    total = total_vehvid + total_murvid + total_thfvid

    counted_v = VehicleVideo.objects.filter(
        uploaded_by__admin_name=user_admin_name).count()
    counted_m = TheftMurderVideo.objects.filter(
        incident='Murder', uploaded_by__admin_name=user_admin_name).count()
    counted_t = TheftMurderVideo.objects.filter(
        incident='Theft', uploaded_by__admin_name=user_admin_name).count()
    total_per_admin = counted_v + counted_m + counted_t

    # count users under the admin(the request user)
    employees_admin = User.objects.filter(
        admin_name=request.user.username, is_active=True).count()

    # Count all admins
    all_admins = User.objects.filter(username=User.admin_name).count()

    # pagination
    veh = VehicleVideo.objects.filter(
        region=request.user.region).order_by('id')
    p = Paginator(veh, 20)
    page = request.GET.get('page')
    veh_list = p.get_page(page)

    context = {'employees_admin': employees_admin, 'all_admins': all_admins,  'total_per_admin': total_per_admin, 'total_vehvid': total_vehvid, 'total_murvid': total_murvid,
               'total_thfvid': total_thfvid, 'total': total, 'counted_v': counted_v, 'counted_m': counted_m, 'counted_t': counted_t, 'veh_list': veh_list}

    return render(request, 'accounts/admind.html', context)


# Super-admin User account Detail Page      ---      accounts/accountdetail.html
@login_required(login_url='login')
def accountdetail(request, pk):
    admins = User.objects.get(id=pk)
    total_standard_users = User.objects.filter(
        admin_name=admins, is_staff=False).count()
    standard_users = User.objects.filter(
        admin_name=admins, is_staff=False).order_by('id')

    p = Paginator(standard_users, 20)
    page = request.GET.get('page')
    acc_detail_list = p.get_page(page)

    context = {'admins': admins, 'total_standard_users': total_standard_users,
               'standard_users': standard_users, 'acc_detail_list': acc_detail_list}
    return render(request, 'accounts/accountdetail.html', context)


# Superadmin Home Page       ---     accounts/superadmin.html
@login_required(login_url='login')
def superadmin(request):
    q = request.GET.get('q')

    if request.GET.get('q') != None:
        Vdata = VehicleVideo.objects.filter(
            Q(title__icontains=q) |
            Q(created__icontains=q) |
            Q(incident__icontains=q) |
            Q(plate_number__icontains=q)
        )
    else:
        Vdata = VehicleVideo.objects.all()
 # _____________________filtering videos .from vehicle, theft .and murder _____________________
    vehvid = VehicleVideo.objects.all()
    total_vehvid = vehvid.count()

    murvid = TheftMurderVideo.objects.filter(incident='Murder')
    total_murvid = murvid.count()

    thfvid = TheftMurderVideo.objects.filter(incident='Theft')
    total_thfvid = thfvid.count()

 # __________________________total videos in total_videos variable_________________
    total_videos = total_vehvid+total_murvid+total_thfvid

 # __________________________total regions_________________
    regions = Regions.objects.all()
    total_regions = regions.count()

 # __________________________total of admin Account's_________________
    adminaccounts = User.objects.filter(is_staff=True)
    total_admins = adminaccounts.count()

 # __________________________total of admin Account's_________________
    accounts = User.objects.all().count()
 # ___________________________set up pagination______________

    # Order the queryset before pagination (assuming 'id' is a field in the Regions model)
    ordered_regions = Regions.objects.order_by('id')

    # Apply pagination to the ordered queryset
    p = Paginator(ordered_regions, 10)
    page = request.GET.get('page')
    region_list = p.get_page(page)

    context = {
        'Vdata': Vdata, 'total_vehvid': total_vehvid, 'total_murvid': total_murvid, 'total_thfvid': total_thfvid, 'total_videos': total_videos, 'regions': regions, 'total_regions': total_regions, 'total_admins': total_admins, 'adminaccounts': adminaccounts, 'accounts': accounts, 'region_list': region_list
    }
    return render(request, 'accounts/superadmin.html', context)


# change user password      ---     accounts/changepwd.html
class UserPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/changepwd.html'
    success_url = reverse_lazy('login')
    logout
    success_message = "Password Changed ✔"


@login_required(login_url='login')
def regions(request, pk):
    region = Regions.objects.get(id=pk)

    vehdetails = VehicleVideo.objects.filter(region=region)
    vehdetail = vehdetails.count()

    thfdetails = TheftMurderVideo.objects.filter(
        incident='Theft', region=region)
    thfdetail = thfdetails.count()

    murdetails = TheftMurderVideo.objects.filter(
        incident='Murder', region=region)
    murdetail = murdetails.count()

    total_per_region = vehdetail + thfdetail+murdetail
    total_user_reg = User.objects.filter(region=region.id).count()

    p = Paginator(VehicleVideo.objects.filter(region=region), 20)
    page = request.GET.get('page')
    veh_reg_list = p.get_page(page)

    context = {'region': region, 'vehdetail': vehdetail, 'vehdetails': vehdetails, 'murdetail': murdetail, 'murdetails': murdetails, 'thfdetail': thfdetail, 'thfdetails': thfdetails, 'total_user_reg': total_user_reg, 'total_per_region': total_per_region, 'veh_reg_list': veh_reg_list
               }
    return render(request, 'accounts/regions.html', context)


@login_required(login_url='login')
def case2datas(request, pk):
    region = Regions.objects.get(id=pk)

    vehdetails = VehicleVideo.objects.filter(region=region)
    vehdetail = vehdetails.count()

    thfdetails = TheftMurderVideo.objects.filter(
        incident='Theft', region=region)
    thfdetail = thfdetails.count()

    murdetails = TheftMurderVideo.objects.filter(
        incident='Murder', region=region)
    murdetail = murdetails.count()

    total_per_region = vehdetail + thfdetail+murdetail
    total_user_reg = User.objects.filter(region=region.id).count()

    p = Paginator(TheftMurderVideo.objects.filter(
        incident='Theft', region=region), 20)
    page = request.GET.get('page')
    theft_reg_list = p.get_page(page)

    context = {'region': region, 'vehdetail': vehdetail, 'vehdetails': vehdetails, 'murdetail': murdetail, 'murdetails': murdetails, 'thfdetail': thfdetail, 'thfdetails': thfdetails, 'total_user_reg': total_user_reg, 'total_per_region': total_per_region, 'theft_reg_list': theft_reg_list
               }
    return render(request, 'base/case2data.html', context)


@login_required(login_url='login')
def case3datas(request, pk):
    region = Regions.objects.get(id=pk)

    vehdetails = VehicleVideo.objects.filter(region=region)
    vehdetail = vehdetails.count()

    thfdetails = TheftMurderVideo.objects.filter(
        incident='Theft', region=region)
    thfdetail = thfdetails.count()

    murdetails = TheftMurderVideo.objects.filter(
        incident='Murder', region=region)
    murdetail = murdetails.count()

    total_per_region = vehdetail + thfdetail+murdetail
    total_user_reg = User.objects.filter(region=region.id).count()

    p = Paginator(TheftMurderVideo.objects.filter(
        incident='Murder', region=region), 20)
    page = request.GET.get('page')
    Mur_reg_list = p.get_page(page)

    context = {'region': region, 'vehdetail': vehdetail, 'vehdetails': vehdetails, 'murdetail': murdetail, 'murdetails': murdetails, 'thfdetail': thfdetail, 'thfdetails': thfdetails, 'total_user_reg': total_user_reg, 'total_per_region': total_per_region, 'Mur_reg_list': Mur_reg_list
               }
    return render(request, 'base/case3data.html', context)


# super-user or staff password reseting to users        ---     accounts/reset.html
@login_required(login_url='login')
def resetpassword(request, pk):
    Edit_password = User.objects.get(id=pk)
    if request.method == 'POST':
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.info(request, "Passwords do not match.")
        elif len(password1) < 8:
            messages.info(
                request, "Password must contain at least 8 characters.")
        else:
            Edit_password.set_password(password1)
            Edit_password.save()
            messages.success(request, 'Password updated successfully !')
    context = {'Edit_password': Edit_password}
    return render(request, 'accounts/reset.html', context)


# super-user or staff deactivating user accounts page       ---     accounts/deleteuser.html
@login_required(login_url='login')
def deleteuser(request, pk):
    user_x = User.objects.get(id=pk)

    if request.method == 'POST':
        User.objects.filter(id=pk).update(
            is_superuser=False, is_staff=False, is_active=False)
        messages.success(request, 'User deleted successfully')
        if request.user.is_superuser:
            return redirect('superadmin')
        else:
            return redirect('usercreation')
    context = {'user': user_x}
    return render(request, 'accounts/deleteuser.html', context)


# Super-user Replace / changeadmin Page       ---         accounts/changeadmin.html
@login_required(login_url='login')
def changeadmin(request, pk):
    admin = User.objects.get(id=pk)

    if request.method == 'POST':
        if admin.is_active == True:
            username = request.POST.get('username')
            if User.objects.filter(username=username).exists():
                messages.success(request, "User Already Exists !!")

            else:
                password = request.POST.get('password')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')

                User.objects.filter(id=pk).update(
                    username=username, first_name=first_name, last_name=last_name)
                Apassword = User.objects.get(id=pk)
                Apassword.password = password
                Apassword.set_password(Apassword.password)
                Apassword.save()

                messages.success(request, "Change's Accepted")
                return redirect('admins')
        else:
            messages.error(
                request, 'Error Happened When changing Admin Status')

    context = {'admin': admin}
    return render(request, 'accounts/changeadmin.html', context)


# download ------------------------------Vehicle--------------------------------
@login_required(login_url='login')
def downloadreasonv(request, pk):
    form = downloadVForm()
    video = VehicleVideo.objects.get(id=pk)
    msg = DownloadedVehicle()

    if request.user.region != "":
        region = request.user.region
    else:
        region = request.user

    if request.method == 'POST':
        form = downloadVForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            current_time = timezone.now()

            previous_downloads = DownloadedVehicle.objects.filter(
                video=video, downloaded_by=request.user, reason=reason)

            if previous_downloads.exists():
                for download in previous_downloads:
                    time_difference = current_time - download.download_time
                    if time_difference.total_seconds() < 300:
                        # Return message that video is already being possessed
                        messages.info(
                            request, 'This video is already being possessed with the same reason. Please try again later.')
                        logout(request)
                        return redirect('login')

            if video.local_plate != None:
                DownloadedVehicle(title=video.title, video=video, uploaded_by=video.uploaded_by, created=video.created, upload=video.upload.date(), incident=video.incident,
                                  local_plate=video.local_plate, plate_region=video.plate_region, plate_number=video.plate_number, region=region, downloaded_by=request.user, reason=reason).save()

                video = get_object_or_404(VehicleVideo, id=pk)
                file_path = video.video.path
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{datetime.now().strftime("%Y-%m-%d")}_{request.user.username}_{request.user.region}.mp4"'
                return response
            else:
                DownloadedVehicle(title=video.title, video=video, uploaded_by=video.uploaded_by, created=video.created, upload=video.upload.date(
                ), incident=video.incident, diplomat_plate=video.diplomat_plate, plate_number=video.plate_number, region=region, downloaded_by=request.user, reason=reason).save()

                video = get_object_or_404(VehicleVideo, id=pk)
                file_path = video.video.path
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='video/mp4')
                response['Content-Disposition'] = f'attachment; filename="{datetime.now().strftime("%Y-%m-%d")}_{request.user.username}_{request.user.region}.mp4"'
                return response

    context = {'form': form, 'video': video}
    return render(request, 'accounts/downloadreason.html', context)

# download --------------------------------------theft murder-----------------------


@login_required(login_url='login')
def downloadtm(request, pk):
    form = downloadTMForm()
    video = TheftMurderVideo.objects.get(id=pk)
    msg = DownloadedTM()

    if request.user.region != "":
        region = request.user.region
    else:
        region = request.user.username

    if request.method == 'POST':
        form = downloadTMForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            current_time = timezone.now()

            previous_downloads = DownloadedTM.objects.filter(
                video=video, downloaded_by=request.user, reason=reason)

            if previous_downloads.exists():
                for download in previous_downloads:
                    time_difference = current_time - download.download_time
                    if time_difference.total_seconds() < 300:
                        # Return message that video is already being possessed
                        messages.info(
                            request, 'This video is already being possessed with the same reason. Please try again later.')
                        logout(request)
                        return redirect('login')

            DownloadedTM(title=video.title, video=video, uploaded_by=video.uploaded_by, created=video.created, upload=video.upload.date(
            ), incident=video.incident, region=region, downloaded_by=request.user, reason=reason).save()

            video = get_object_or_404(TheftMurderVideo, id=pk)
            file_path = video.video.path
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='video/mp4')
            response['Content-Disposition'] = f'attachment; filename="{datetime.now().strftime("%Y-%m-%d")}_{request.user.username}_{request.user.region}.mp4"'
            return response

    context = {'form': form, 'video': video}
    return render(request, 'accounts/downloadreasontm.html', context)


@login_required(login_url='login')
def downloadveh(request):
    video = DownloadedVehicle.objects.all().order_by('id')
    total_dVideo = video.count()

    p = Paginator(video, 25)
    page = request.GET.get('page')
    video_list = p.get_page(page)
    context = {'video': video_list, 'total_dVideo': total_dVideo}
    return render(request, 'accounts/downloads.html', context)


@login_required(login_url='login')
def downloadTh(request):
    video = DownloadedTM.objects.filter(incident="Theft").order_by('id')
    total_dVideo = video.count()

    p = Paginator(video, 25)
    page = request.GET.get('page')
    video_list = p.get_page(page)
    context = {'video': video_list, 'total_dVideo': total_dVideo}
    return render(request, 'accounts/downloadedt.html', context)


@login_required(login_url='login')
def downloadMr(request):
    video = DownloadedTM.objects.filter(incident="Murder").order_by('id')
    total_dVideo = video.count()

    p = Paginator(video, 25)
    page = request.GET.get('page')
    video_list = p.get_page(page)
    context = {'video': video_list, 'total_dVideo': total_dVideo}
    return render(request, 'accounts/downloadedm.html', context)


@login_required(login_url='login')
def downloaded_detail(request, pk):
    video = DownloadedVehicle.objects.get(id=pk)
    downloaded_video = video.video.id
    selected_video = VehicleVideo.objects.get(id=downloaded_video)
    display = selected_video.video

    context = {'video': video, 'display': display}
    return render(request, 'accounts/downloaded_detail.html', context)


@login_required(login_url='login')
def downloaded_detail2(request, pk):
    video = DownloadedTM.objects.get(id=pk)
    downloaded_video = video.video.id
    selected_video = TheftMurderVideo.objects.get(id=downloaded_video)
    display = selected_video.video

    context = {'video': video, 'display': display}
    return render(request, 'accounts/downloaded_detail2.html', context)


# super-user user log time      ---      accounts/logs.html
@login_required(login_url='login')
def accountlogs(request):
    # users = User.objects.all().order_by('-last_login')
    users = User.objects.filter(
        last_login__isnull=False).order_by('-last_login')

    # p = Paginator(u, 25)
    p = Paginator(users, 25)
    page = request.GET.get('page')
    user_list = p.get_page(page)

    # context = {'users': u, 'user_list': user_list}
    context = {'users': users, 'user_list': user_list}

    return render(request, 'accounts/logs.html', context)


# super-user API - user creation Form       ---     accounts/superadmin-api.html
# super-user API - user creation Form --- accounts/superadmin-api.html
@login_required(login_url='login')
def superadminapi(request):
    form = superusercreationForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        
        # print(f"Password: {password}")
        # print(f"Password Confirm: {password_confirm}")

        if password != password_confirm:
            messages.error(request, 'Password and password confirmation do not match.')
            return redirect('superadmin-api')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'USERNAME ALREADY EXISTS !!')
            return redirect('superadmin-api')

        try:
            # Validate password using Django's built-in validators
            validate_password(password, user=User)
            uppercase_validator = UppercaseValidator()
            lowercase_validator = LowercaseValidator()
            symbol_validator = SymbolValidator()
            length_validator = MinimumLengthValidator(min_length=8)

            uppercase_validator.validate(password)
            lowercase_validator.validate(password)
            symbol_validator.validate(password)
            length_validator.validate(password)
        
        except ValidationError as e:
            messages.error(request, '\n'.join(e.messages))
            return redirect('superadmin-api')
        if User.objects.filter(is_superuser=True).count() <= 3:
                User.objects.create_user(
                    username=username,
                    first_name=firstname,
                    last_name=lastname,
                    password=password,
                    is_active=True,
                    is_staff=True,
                    is_superuser=True
                )
                messages.info(request, 'Superadmin Account Created !!')
        else:
                messages.info(request, 'Maximum allowed superadmins reached')
       

    context = {'form': form}
    return render(request, 'accounts/superadmin-api.html', context)



@login_required(login_url='login')
def get_apiuser(request):
    apiuser = User.objects.filter(email__gt='', email__isnull=False)
    apiuser_total = apiuser.count()

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.info(request, "User Already Exists")
        elif User.objects.filter(email=email).exists():
            messages.info(request, "Email Already Taken")
        else:
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname,
                                            password=password, email=email, is_staff="False", is_superuser="False")

            user.save()

            messages.info(request, "Api User Created Successfully")

    api_users = Token.objects.all()

    context = {'apiuser': apiuser,
               'apiuser_total': apiuser_total, 'api_users': api_users}
    return render(request, 'accounts/api-user.html', context)


@login_required(login_url='login')
def api_activation(request, pk):

    user = User.objects.get(id=pk)

    if user is not None:
        try:
            token = Token.objects.get(user_id=user.id)
            messages.info(request, 'User Token Already Created !')

        except Token.DoesNotExist:

            if user.is_superuser == False:
                if user.is_staff == False:
                    if User.objects.filter(id=pk, email__gt='', email__isnull=False):
                        token = Token.objects.create(user=user)
                        messages.info(request, 'Token Created Successfully !')
                else:
                    messages.info(request, 'Cannot Assign to the user!')
            else:
                messages.info(request, 'Cannot Assign to the user!')

    context = {'tokenuser': token, }
    return render(request, 'accounts/api_activation.html', context)
