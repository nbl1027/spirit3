from django.shortcuts import render, get_object_or_404, redirect
from .models import Patientinfo
from spirit3.forms import PatientForm
from django.contrib.auth import authenticate, login 
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


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

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return redirect('home')
			else:
				return HttpResponse("Your SPIRIT 3 account is disabled")

		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'spirit3/login.html',{})


@login_required
def restricted(request):	
	return HttpResponse("Since you're logged in you can see this text")

