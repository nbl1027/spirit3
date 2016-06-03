from django.shortcuts import render
from .models import Patientinfo

def patient_list(request):
	patient_list = Patientinfo.objects.all()
	return render(request, 'spirit3/patient_list.html', {'patient_list': patient_list}) 

# Create your views here.
