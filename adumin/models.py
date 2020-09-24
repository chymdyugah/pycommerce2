from django.db import models
from irish.models import Product

# Create your models here.


class Refill(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField('Refill Quantity')
	date = models.DateField('Refill Date', auto_now_add=True)

	def __str__(self):
		return self.product.name

