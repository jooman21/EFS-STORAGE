from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid




class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin_name = models.CharField(max_length=50, null=True)
    region = models.ForeignKey('Regions', max_length=100, on_delete=models.DO_NOTHING,null=True)
  


class Regions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    created_by= models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    def __str__(self): 
        return self.name
