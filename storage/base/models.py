from django.db import models
from .validators import file_size
from django.core.validators import FileExtensionValidator
from accounts.models import User,Regions
import uuid


class VehiclePlateLocal(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plate_id = models.CharField(max_length=3)
    plate_name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT)

    def __str__(self): 
        return self.plate_name

class VehiclePlateCD(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plate_id = models.CharField(max_length=3)
    plate_name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    
    def __str__(self): 
        return self.plate_id

class VehicleRegion(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region_name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    
    def __str__(self): 
        return self.region_name



class VehicleVideo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to="Evidences/%y/%m",validators=[file_size, FileExtensionValidator( ['mp4'] )] )
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='VehicleVideo_uploaded_by')
    created = models.CharField(max_length=50, null=True)
    upload = models.DateTimeField(auto_now_add=True)
    incident = models.CharField(max_length=12)
    local_plate = models.ForeignKey(VehiclePlateLocal, null=True, on_delete=models.PROTECT,blank=True)
    plate_region = models.ForeignKey(VehicleRegion, null=True, on_delete=models.PROTECT,blank=True)
    plate_number = models.CharField(max_length=6)
    diplomat_plate = models.ForeignKey(VehiclePlateCD, null=True, on_delete=models.PROTECT,blank=True)
    region = models.ForeignKey(Regions, on_delete=models.DO_NOTHING, null=True,blank=True)

    class Meta:
        ordering = ['-upload', '-created']

    def __str__(self): 
        return self.title

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)    

class TheftMurderVideo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to="Evidences/%y/%m", validators=[file_size, FileExtensionValidator( ['mp4'] )] )
    uploaded_by= models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='TheftMurderVideo_uploaded_by')
    created = models.CharField(max_length=50, null=True)
    upload = models.DateTimeField(auto_now_add=True)
    incident=models.CharField(max_length=6)
    region = models.ForeignKey(Regions, on_delete=models.DO_NOTHING, null=True,blank=True)

    class Meta:
        ordering = ['-upload', '-created']

    def __str__(self): 
        return self.title
    
    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)  



class DeletedVehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to="Evidences/Deleted/%y/%m")
    uploaded_by= models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='DeletedVehicle_uploaded_by')
    created = models.CharField(max_length=50,)
    upload = models.CharField(max_length=50,)
    incident=models.CharField(max_length=12)
    local_plate = models.ForeignKey(VehiclePlateLocal, null=True, on_delete=models.PROTECT,blank=True)   
    plate_region = models.ForeignKey(VehicleRegion, null=True, on_delete=models.PROTECT,blank=True)
    plate_number = models.CharField(max_length=6)
    diplomat_plate  = models.ForeignKey(VehiclePlateCD, null=True, on_delete=models.PROTECT,blank=True)
    deleted_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='DeletedVehicle_deleted_by')
    deleted_time = models.DateTimeField(auto_now_add=True)
    region = models.ForeignKey(Regions, on_delete=models.DO_NOTHING, null=True,blank=True)
    reason = models.TextField(max_length=150)
    number_of_download = models.IntegerField()

    class Meta:
        ordering = ['-upload', '-created']

    def __str__(self): 
        return self.title

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)     

class DeletedTM(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to="Evidences/Deleted/%y/%m")
    uploaded_by= models.ForeignKey(User, null=True, on_delete=models.PROTECT,related_name='DeletedTM_uploaded_by')
    created = models.CharField(max_length=50, )
    upload = models.CharField(max_length=50,)
    incident=models.CharField(max_length=6)
    region = models.ForeignKey(Regions, on_delete=models.DO_NOTHING, null=True,blank=True)
    deleted_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT,related_name='DeletedTM_deleted_by')
    deleted_time = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(max_length=150)
    number_of_download = models.IntegerField()
    class Meta:
        ordering = ['-upload', '-created']

    def __str__(self): 
        return self.title

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)



class DownloadedVehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    video = models.ForeignKey(VehicleVideo, null=True, on_delete=models.CASCADE, default="visited")
    uploaded_by= models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='DownloadedVehicle_uploaded_by')
    created = models.CharField(max_length=50,)
    upload = models.CharField(max_length=50,)
    incident=models.CharField(max_length=12)
    local_plate = models.ForeignKey(VehiclePlateLocal, null=True, on_delete=models.PROTECT,blank=True)
    plate_region = models.ForeignKey(VehicleRegion, null=True, on_delete=models.PROTECT,blank=True)
    plate_number = models.CharField(max_length=6)
    diplomat_plate  = models.ForeignKey(VehiclePlateCD, null=True, on_delete=models.PROTECT,blank=True)
    region = models.ForeignKey(Regions, on_delete=models.DO_NOTHING, null=True,blank=True)
    downloaded_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT,blank=True ,related_name='DownloadedVehicle_downloaded_by')
    download_time = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(max_length=250)

    class Meta:
        ordering = ['-download_time']

    def __str__(self): 
        return self.title   

class DownloadedTM(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    video = models.ForeignKey(TheftMurderVideo, null=True, on_delete=models.CASCADE, default="visited")
    uploaded_by= models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='DownloadedTM_uploaded_by')
    created = models.CharField(max_length=50, )
    upload = models.CharField(max_length=50,)
    incident=models.CharField(max_length=6)
    region = models.ForeignKey(Regions, on_delete=models.DO_NOTHING, null=True,blank=True)
    downloaded_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name='DownloadedTM_downloaded_by')
    download_time = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(max_length=150)

    class Meta:
        ordering = ['-upload', '-created']

    def __str__(self): 
        return self.title
