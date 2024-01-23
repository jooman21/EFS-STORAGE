from rest_framework import serializers
from base.models import *
from accounts.models import User, Regions
from django.contrib.auth import get_user_model
User = get_user_model()

class RegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regions
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    region = RegionsSerializer()
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','region') 



class VehicleRegionSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    class Meta:
        model = VehicleRegion
        fields = '__all__'

class LocalPlateSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    class Meta:
        model = VehiclePlateLocal
        fields = '__all__'

class CDPlateSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    class Meta:
        model = VehiclePlateCD()
        fields = '__all__'



class VehicleVideoSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer()
    local_plate= LocalPlateSerializer()
    plate_region= VehicleRegionSerializer()
    diplomat_plate= CDPlateSerializer()
    region = RegionsSerializer()
    class Meta:
        model = VehicleVideo
        fields = '__all__'

class TheftMurderVideoSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer()
    region = RegionsSerializer()

    class Meta:
        model = TheftMurderVideo
        fields = '__all__'



class DeletedVehicleSerializer(serializers.ModelSerializer):
    deleted_by = UserSerializer()
    local_plate= LocalPlateSerializer() 
    diplomat_plate= CDPlateSerializer()
    plate_region= VehicleRegionSerializer()
    uploaded_by = UserSerializer()
    region = RegionsSerializer()
    class Meta:
        model = DeletedVehicle
        fields = '__all__'

class DeletedTMSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer()
    region = RegionsSerializer()
    deleted_by = UserSerializer()
    class Meta:
        model = DeletedTM
        fields = '__all__'



class DownloadedVehicleSerializer(serializers.ModelSerializer):
    video = VehicleVideoSerializer()
    uploaded_by = UserSerializer()
    local_plate= LocalPlateSerializer() 
    diplomat_plate= CDPlateSerializer()
    plate_region= VehicleRegionSerializer()
    region = RegionsSerializer()
    downloaded_by = UserSerializer()
    class Meta:
        model = DownloadedVehicle
        fields = '__all__'

class DownloadedTMSerializer(serializers.ModelSerializer):
    video = VehicleVideoSerializer()
    uploaded_by = UserSerializer()
    region = RegionsSerializer()
    downloaded_by = UserSerializer()
    class Meta:
        model = DownloadedTM
        fields = '__all__'
