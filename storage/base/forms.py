from django.forms import ModelForm, Select
from .models import *
from django.core.exceptions import ValidationError
from django import forms

class VehicleForm(ModelForm):
  class Meta:
    model = VehicleVideo
    fields = '__all__'
    widgets = {
      'local_plate': Select(attrs={'required': 'required'}),
      'plate_region': Select(attrs={'required': 'required'})
      }
    exclude = ['title','created','incident','uploaded_by','region','diplomat_plate']

class VehicleFormcd(ModelForm):
  class Meta:
    model = VehicleVideo
    fields = '__all__'
    widgets = {
      'diplomat_plate': Select(attrs={'required': 'required'}),
      'plate_region': Select(attrs={'required': 'required'})
      }
    exclude = ['title','local_plate','plate_region','created','incident','uploaded_by','region']

class TheftMurderForm(ModelForm):
  class Meta:
    model = TheftMurderVideo
    fields ='__all__'  
    exclude = ['title','created','incident','uploaded_by','region']  

class dvehForm(ModelForm):
  class Meta:
    model = DeletedVehicle
    fields =['reason']
  
  def clean_reason(self):
    reason = self.cleaned_data['reason']
    if not reason or len(reason) < 15:
      raise forms.ValidationError("Please provide a valid and meaningful reason (minimum 15 characters).")
    return reason  
  

class dTMForm(ModelForm):
  class Meta:
    model = DeletedTM
    fields =['reason']

def clean_reason(self):
    reason = self.cleaned_data['reason']
    if not reason or len(reason) < 15:
      raise forms.ValidationError("Please provide a valid and meaningful reason (minimum 15 characters).")
    return reason


class downloadVForm(ModelForm):
  class Meta:
    model = DownloadedVehicle
    fields =['reason']

def clean_reason(self):
    reason = self.cleaned_data['reason']
    if not reason or len(reason) < 15:
      raise forms.ValidationError("Please provide a valid and meaningful reason (minimum 15 characters).")
    return reason


class downloadTMForm(ModelForm):
  class Meta:
    model = DownloadedTM
    fields =['reason']

def clean_reason(self):
    reason = self.cleaned_data['reason']
    if not reason or len(reason) < 15:
      raise forms.ValidationError("Please provide a valid and meaningful reason (minimum 15 characters).")
    return reason    