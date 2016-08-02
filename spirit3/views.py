#***** Imports libraries *****
import csv
import mysql.connector
from datetime import datetime
import numpy as np
from django.shortcuts import render, get_object_or_404, redirect
from .models import Patientinfo
from spirit3.forms import PatientForm, ResultUpload
from django.contrib.auth import authenticate, login, logout 
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction
from spirit3.functions import *


#***** Database Connection & Cursor *****
cnx = mysql.connector.connect(user='kirsty', password='ngskirsty_201605', host='10.229.233.250', database = 'spirit3')
cursor = cnx.cursor()


#**** View Functions *****

#Handles the uploaded results file from the upload from
def handle_uploaded_file(results):
		csv_f = csv.reader(results)
		plateresult = [row for row in csv_f]
		platedate(plateresult)
		resultsort(plateresult)
		standardsort(standards)
		for row in controls:
			if len(row) == 11:
				del row[2]
		for row in samples:
			if len(row) == 11:
				del row[2]
		insertcontrols(controls)
		insertstandards(standardresults)
		insertsamples(samples)

#****** Views ********

#Displats a list of patients
def patient_list(request):
	patient_list = Patientinfo.objects.all()
	return render(request, 'spirit3/patient_list.html', {'patient_list': patient_list}) 

#Displays detail of patients (BROKE)
def patient_detail(request, pk):
	patient_detail = get_object_or_404(Patientinfo.objects.all(), pk=pk)
	return render(request, 'spirit3/patient_detail.html', {'patient_list':patient_list})

#Displays the homepage
def home(request):
	return render(request, 'spirit3/home.html')

#Allows user to add a patient to the database
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

#Login form for the user
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


#Allows the user to upload the results 
def result_upload(request):
	if request.method == 'POST':
		form = ResultUpload(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['results'])
			return HttpResponseRedirect('/')
		else:
			print form.errors
	else:
		form = ResultUpload()
	return render(request, 'spirit3/result_upload.html', {'form':form})
	

#***** Python decorators ******

@login_required
def restricted(request):	
	return HttpResponse("Since you're logged in you can see this text")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

