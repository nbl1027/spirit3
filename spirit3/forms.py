from django import forms
from .models import Patientinfo

class PatientForm(forms.Modelform):
    nhsnumber = forms.IntegerField(help_text="Please enter nhs number")
    #initials = forms.CharField(help_text="Please enter patient initials"))
    #dob = forms.DateField(help_text="Please enter patient D.O.B")

    class Meta:
        model = Patientinfo
	fields = ('nhsnumber')
