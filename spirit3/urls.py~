from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'), 
	url(r'^patientlist', views.patient_list, name='patient_list'), 
	url(r'^patientdetail/(?P<pk>\d+)/$', views.patient_detail, name='patient_detail'), 
	url(r'^add_patient/$', views.add_patient, name='add_patient'),
	url(r'^login/$', views.user_login, name='login'), 
	url(r'^restricted/', views.restricted, name='restricted'),
]


