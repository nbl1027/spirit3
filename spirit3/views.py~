from django.shortcuts import render, get_object_or_404, redirect
from .models import Patientinfo
from spirit3.forms import PatientForm, ResultUpload
from django.contrib.auth import authenticate, login, logout 
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
import mysql.connector

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
				return HttpResponseRedirect('/')
			else:
				return HttpResponse("Your SPIRIT 3 account is disabled")

		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'spirit3/login.html',{})


def result_upload(request):
	if request.method == 'POST':
		form = ResultUpload(request.POST, request.FILES)
		from spirit3.plateqc import *
		from spirit3.results import *
		from spirit3.sampleresult import *
		#if form.is_valid():
			#handle_uploaded_file(request.FILES['file']) Need to define handle file function
			#return HttpResponseRedirect('/')
		#else:
			#form = ResultUpload()
		return render(request, 'result_upload.html', {'form':form})
	





##Python decorators 

@login_required
def restricted(request):	
	return HttpResponse("Since you're logged in you can see this text")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

