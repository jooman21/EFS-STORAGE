from django.forms import ModelForm, TextInput,Select
from .models import User,Regions,AbstractUser
from django import forms


class CreateRegionForm(ModelForm):
  class Meta:
    model = Regions
    fields = ['name'] 

class CreateUserForm(ModelForm):
   password = forms.CharField(widget=forms.PasswordInput)
   password_confirm = forms.CharField(widget=forms.PasswordInput)

   class Meta:
    model = User
    widgets = {
      'first_name': TextInput(attrs={'required': 'required'}),
      'last_name': TextInput(attrs={'required': 'required'}),
      }
    fields = ['username','first_name','last_name','password','password_confirm']
   
class createAdminForm(ModelForm):
  password = forms.CharField(widget=forms.PasswordInput)
  password_confirm = forms.CharField(widget=forms.PasswordInput)
  class Meta:
    model = User
    widgets = {
      'first_name': TextInput(attrs={'required': 'required'}),
      'last_name': TextInput(attrs={'required': 'required'}),
      'region': Select(attrs={'required': 'required'})
      }
    fields = ['username','first_name','last_name','password','password_confirm','region']

class superusercreationForm(ModelForm):
  password = forms.CharField(widget=forms.PasswordInput)
  password_confirm = forms.CharField(widget=forms.PasswordInput)
  class Meta:
    model = User
    widgets = {
      'first_name': TextInput(attrs={'required': 'required'}),
      'last_name': TextInput(attrs={'required': 'required'})
      }
    fields = ['username','first_name','last_name','password', 'password_confirm']

class passwordeditform(ModelForm):
  class Meta:
    model = User
    fields = ['password']  


class useraccountForm(ModelForm):
  class Meta:
    model = User 
    fields = ['username','first_name','last_name','is_superuser','is_staff','is_active' ,'admin_name','region','password']   