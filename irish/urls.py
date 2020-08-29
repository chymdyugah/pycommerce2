from django.conf.urls import url
from . import views

app_name = "irish"

urlpatterns = [
	url('^$', views.Index.as_view(), name='index'),
	url('^cart/$', views.CartView.as_view(), name='cart'),
	url('^checkout/$', views.Checkout.as_view(), name='checkout'),
	url('^single/(?P<pk>[0-9]+)/$', views.Single.as_view(), name='single'),
	url('^login/$', views.Login.as_view(), name='login'),
	url('^register/$', views.Registration.as_view(), name='register'),
	url('^logout/$', views.LogoutV.as_view(), name='logout'),
	url('^ajx/$', views.AjxView.as_view(), name='ajx'),
]
