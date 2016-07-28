from django.shortcuts import render, get_object_or_404, redirect
from .models import Patientinfo
from spirit3.forms import PatientForm


def patient_list(request):
	patient_list = Patientinfo.objects.all()
	return render(request, 'spirit3/patient_list.html', {'patient_list': patient_list}) 

def patient_detail(request, pk):
	patient_detail = get_object_or_404(Patientinfo.objects.all(), pk=pk)
	return render(request, 'spirit3/patient_detail.html', {'patient_list':patient_list})

def home(request):
	return render(request, 'spirit3/home.html')

def add_patient(request):
	if request.method == 'POST':
		form = PatientForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return redirect('home')
		else:
			print form.errors
	else:
		form = PatientForm()
	return render(request, 'spirit3/add_patient.html', {'form':form})
