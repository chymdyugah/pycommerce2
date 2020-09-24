from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
	prodid = models.CharField(max_length=255, default='prod0')
	name = models.CharField(max_length=255)
	price = models.IntegerField(default=0)
	quantity = models.IntegerField(default=0)
	categories = models.CharField(max_length=255)
	description = models.CharField(max_length=500)
	image = models.ImageField(default="null")

	def __str__(self):
		return self.name


class Cart(models.Model):
	cart_id = models.IntegerField(default=0)
	prodid = models.CharField(max_length=10)
	prod_name = models.CharField(max_length=255)
	quantity = models.IntegerField(default=1)
	total = models.IntegerField(default=0)
	status = models.CharField(max_length=255, default="")
	date = models.DateField(auto_now_add=True, null=True)

	def __str__(self):
		return self.prodid


class Shipment(models.Model):
	order = models.CharField(verbose_name='Order id', max_length=20)
	address = models.TextField('Delivery Address')
	items = models.TextField('Items Ordered')
	status = models.CharField(verbose_name='Status', max_length=20)
	date = models.DateField('Order Date', auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, default='')

	def __str__(self):
		return self.order
