from django.shortcuts import render
from .models import Patientinfo

def patient_list(request):
	patients = Patientinfo.objects.all()
	return render(request, 'spirit3/patient_list.html', {}) 

# Create your views here.
