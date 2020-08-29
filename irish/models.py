from django.db import models

# Create your models here.


class Product(models.Model):
	name = models.CharField(max_length=255)
	price = models.IntegerField(default=0)
	quantity = models.IntegerField(default=0)
	categories = models.CharField(max_length=255)
	description = models.CharField(max_length=500)
	image = models.FileField(default="null")

	def __str__(self):
		return self.name


class Cart(models.Model):
	cart_id = models.IntegerField(default=0)
	prodid = models.CharField(max_length=10)
	prod_name = models.CharField(max_length=255)
	quantity = models.IntegerField(default=1)
	total = models.IntegerField(default=0)
	status = models.CharField(max_length=255, default="")

	def __str__(self):
		return self.prodid
