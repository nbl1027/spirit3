from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.patient_list, name='patient_list'), 
	url(r'^patient/(?P<pk>\d+)/$', views.patient_detail, name='patient_detail'), 
]


