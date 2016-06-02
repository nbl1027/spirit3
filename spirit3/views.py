from django.shortcuts import render

def patient_list(request):
	return render(request, 'spirit3/patient_list.html', {})

# Create your views here.
