from django.conf.urls import url
from . import views

app_name = "irish"

urlpatterns = [
	url('^$', views.Index.as_view(), name='index'),
	url('^shop/$', views.Shop.as_view(), name='shop'),
	url('^shop/(?P<cat>\w+)/$', views.Category.as_view(), name='category'),
	url('^cart/$', views.CartView.as_view(), name='cart'),
	url('^checkout/$', views.Checkout.as_view(), name='checkout'),
	url('^single/(?P<pk>[a-z0-9]+)/$', views.Single.as_view(), name='single'),
	url('^login/$', views.Login.as_view(), name='login'),
	url('^register/$', views.Registration.as_view(), name='register'),
	url('^logout/$', views.LogoutV.as_view(), name='logout'),
	url('^ajx/$', views.AjxView.as_view(), name='ajx'),
]
