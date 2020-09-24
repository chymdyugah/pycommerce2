from django.conf.urls import url
from . import views

app_name = "adumin"

urlpatterns = [
	url('^$', views.Index.as_view(), name='index'),
	url('^login/$', views.Login.as_view(), name='login'),
	url('^logout/$', views.Logout.as_view(), name='logout'),
	url('^register/$', views.Registration.as_view(), name='register'),
	url('^inventory/$', views.Inventory.as_view(), name='inventory'),
	url('^refill/$', views.RefillView.as_view(), name='refill'),
	url('^redr/$', views.Redr.as_view(), name='redr'),
	url('^inventcharts/$', views.InventCharts.as_view(), name='inventcharts'),
	url('^ajx/$', views.Ajx.as_view(), name='ajx'),
]
