from django import forms
from django.db import models
from .models import Patientinfo

class PatientForm(forms.ModelForm):
    nhsnumber = forms.IntegerField
    initials = forms.CharField
    dob = forms.DateField

    class Meta:
        model = Patientinfo
	fields = ('nhsnumber', 'initials', 'dob')


class ResultUpload(forms.Form):
	file = forms.FileField()
