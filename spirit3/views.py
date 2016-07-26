from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Patientinfo


def patient_list(request):
	patient_list = Patientinfo.objects.all()
	return render(request, 'spirit3/patient_list.html', {'patient_list': patient_list}) 

def patient_detail(request, pk):
	patient = get_object_or_404(Patientinfo, pk=pk)
	return render(request, 'spirit3/patient_detail.html', {'patient_list':patient_list})




