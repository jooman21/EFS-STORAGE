from django.core.exceptions import ValidationError
# from django import forms
# from .models import DeletedVehicle
# this is only check if the data is >3mv

def file_size(value):
   filesize = value.size
   if filesize < 3000000:
       raise ValidationError("minimum size is 3mb")


# forms.py



# class DvehForm(forms.ModelForm):
#     class Meta:
#         model = DeletedVehicle
#         fields = ['reason']
#         widgets = {
#             'reason': forms.Textarea(attrs={'rows': 3}),
#         }

#     def clean_reason(self):
#         reason = self.cleaned_data['reason']
#         if not reason or len(reason) < 5:  # Adjust the condition based on your requirements
#             raise forms.ValidationError("Please provide a valid and meaningful reason (minimum 5 characters).")
#         return reason
    