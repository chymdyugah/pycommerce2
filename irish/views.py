from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
import random
from pycommerce.settings import LOGIN_REDIRECT_URL
from .models import Product, Cart, Shipment
from .forms import LoginForm, RegistrationForm
from django.db.models import Sum
import datetime

# Create your views here.


class Index(generic.ListView):
	template_name = 'irish/index.html'

	def get(self, request, *args, **kwargs):
		if 'id' not in request.session:
			request.session['id'] = random.randint(999, 9999999)
			request.session['id'] = hash(datetime.datetime.now())

		products = Product.objects.all()[0:12]
		cart = Cart.objects.filter(cart_id=request.session['id'], status='').count()
		sess = request.session['id']
		return render(request, self.template_name, {'products': products, 'cart': cart, 'sess': sess})


class Shop(generic.ListView):
	template_name = 'irish/shop.html'

	def get(self, request, *args, **kwargs):
		if 'id' not in request.session:
			request.session['id'] = random.randint(999, 9999999)
			request.session['id'] = hash(datetime.datetime.now())
			products_per_page = 1  # change this variable to set the number of items in page

		if 'p1' in request.GET:
			if 'n' in request.GET:
				n = int(request.GET['n'])
				start_prod = n * products_per_page - products_per_page
				end_prod = n * products_per_page

				products = Product.objects.filter(price__gte=request.GET['p1'], price__lte=request.GET['p2'])[start_prod:end_prod]
			else:
				n = 1
				products = Product.objects.filter(price__gte=request.GET['p1'], price__lte=request.GET['p2'])[0:products_per_page]
		else:
			if 'n' in request.GET:
				n = int(request.GET['n'])
				start_prod = n * products_per_page - products_per_page
				end_prod = n * products_per_page
				products = Product.objects.all()[start_prod:end_prod]
			else:
				n = 1
				products = Product.objects.all()[0:products_per_page]
		if 'desc' in request.GET:
			products = Product.objects.filter(description__contains=request.GET['desc'])[0:products_per_page]
			if 'n' in request.GET:
				n = int(request.GET['n'])
				start_prod = n * products_per_page - products_per_page
				end_prod = n * products_per_page
				products = Product.objects.filter(description__contains=request.GET['desc'])[start_prod:end_prod]

		cart = Cart.objects.filter(cart_id=request.session['id'], status='').count()
		sess = request.session['id']
		if len(products) == 0:
			return render(request, self.template_name, {'err': 'No more Product'})

		return render(request, self.template_name, {'products': products, 'cart': cart, 'sess': sess, 'nxt': n+1, 'prv': n-1})


class Category(generic.ListView):
	template_name = 'irish/shop.html'

	def get(self, request, cat, *args, **kwargs):
		if 'id' not in request.session:
			request.session['id'] = random.randint(999, 9999999)
			request.session['id'] = hash(datetime.datetime.now())
			products_per_page = 1

		if 'p1' in request.GET:
			if 'n' in request.GET:
				n = int(request.GET['n'])
				start_prod = n * products_per_page - products_per_page
				end_prod = n * products_per_page
				products = Product.objects.filter(price__gte=request.GET['p1'], price__lte=request.GET['p2'], categories__contains=cat)[start_prod:end_prod]
			else:
				n = 1
				products = Product.objects.filter(price__gte=request.GET['p1'], price__lte=request.GET['p2'], categories__contains=cat)[0:products_per_page]
		else:
			if 'n' in request.GET:
				n = int(request.GET['n'])
				start_prod = n * products_per_page - products_per_page
				end_prod = n * products_per_page
				products = Product.objects.filter(categories__contains=cat)[start_prod:end_prod]
			else:
				n = 1
				products = Product.objects.filter(categories__contains=cat)[0:products_per_page]

		cart = Cart.objects.filter(cart_id=request.session['id'], status='').count()
		sess = request.session['id']
		if len(products) == 0:
			return render(request, self.template_name, {'err': 'No more Product'})

		return render(request, self.template_name, {'products': products, 'cart': cart, 'sess': sess, 'nxt': n+1, 'prv': n-1})


class CartView(generic.ListView):
	template_name = 'irish/cart.html'

	def get(self, request, *args, **kwargs):
		if 'id' not in request.session:
			request.session['id'] = random.randint(999, 9999999)
			request.session['id'] = hash(datetime.datetime.now())

		sess = request.session['id']
		products = Cart.objects.filter(cart_id=request.session['id'], status="")
		cart = Cart.objects.filter(cart_id=request.session['id'], status="").count()
		subtotal = Cart.objects.filter(cart_id=request.session['id'], status="").aggregate(Sum('total'))
		subtotal = subtotal['total__sum']
		if subtotal is None:
			subtotal = ""
		final = ""
		for product in products:
			final += product.prod_name+","+str(product.quantity)+";"

		return render(request, self.template_name, {'cart': cart, 'products': products, 'subtotal': subtotal, 'final': final, 'sess': sess})


@method_decorator(login_required, name='dispatch')
class Checkout(View):
	template_name = 'irish/checkout.html'

	def get(self, request):
		if 'id' not in request.session:
			request.session['id'] = random.randint(999, 9999999)
			request.session['id'] = hash(datetime.datetime.now())

		sess = request.session['id']
		products = Cart.objects.filter(cart_id=request.session['id'], status="")
		cart = Cart.objects.filter(cart_id=request.session['id'], status="").count()
		subtotal = Cart.objects.filter(cart_id=request.session['id'], status="").aggregate(Sum('total'))
		subtotal = subtotal['total__sum']
		if subtotal is None:
			subtotal = ""
		final = ""
		for product in products:
			final += product.prod_name + "," + str(product.quantity) + ";"

		return render(request, self.template_name, {'cart': cart, 'products': products, 'subtotal': subtotal, 'final': final, 'sess': sess})


class Single(generic.DetailView):
	template_name = 'irish/single.html'
	model = Product

	def get(self, request, pk, *args, **kwargs):
		if 'id' not in request.session:
			request.session['id'] = random.randint(999, 9999999)
			request.session['id'] = hash(datetime.datetime.now())
		try:
			prod = Product.objects.get(prodid=pk)
		except Product.DoesNotExist:
			return redirect('irish:index')

		cart = Cart.objects.filter(cart_id=request.session['id'], status="").count()
		sess = request.session['id']
		return render(request, self.template_name, {'product': prod, 'cart': cart, 'sess': sess})


class Login(View):
	template_name = 'irish/login3.html'
	form_class = LoginForm

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					if 'next' in request.GET:
						return redirect(request.GET['next'])
					else:
						return redirect(LOGIN_REDIRECT_URL)

			err = 'Wrong Username or Password'
		return render(request, self.template_name, {'form': form, 'err': err})


class Registration(View):
	template_name = 'irish/signup.html'
	form_class = RegistrationForm

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('irish:index')

		return render(request, self.template_name, {'form': form})


class LogoutV(View):
	def get(self, request):
		Cart.objects.filter(cart_id=request.session['id'], status='').delete()
		logout(request)
		return redirect('irish:index')


# ajax view
class AjxView(View):

	def get(self, request):
		# change the quantity of a product in cart
		if 'quant' in request.GET:
			pid = request.GET['serial']
			quant = int(request.GET['quant'])
			product = Cart.objects.get(pk=pid)
			sel_prod = Product.objects.get(prodid=product.prodid)
			price = sel_prod.price
			total = price * quant
			product.quantity = quant
			product.total = total
			product.save()

			return HttpResponse(total)

		# deletes a product from cart
		if "sn" in request.GET:
			pid = request.GET['sn']
			Cart.objects.get(pk=pid).delete()

			return HttpResponse('done')

		# clear cart
		if "clear" in request.GET:
			kart = request.session['id']
			Cart.objects.filter(cart_id=kart, status='').delete()

			return HttpResponse('done')

	def post(self, request):
		# adds a product to cart
		if 'pid' in request.POST:
			pid = request.POST['pid']
			name = request.POST['name']
			price = request.POST['price']
			cart = request.POST['cart']
			pro = Cart.objects.filter(cart_id=cart, status="", prodid=pid).count()
			if pro is 0:
				new_cart = Cart.objects.create(cart_id=cart, prod_name=name, prodid=pid, total=price)
				new_cart.save()
			data = Cart.objects.filter(cart_id=cart).count()
			return HttpResponse(data)

		# finalizes your order after successful payment and subtracts the quantity of the products from Product
		if 'up' in request.POST:
			order = request.POST['order']
			cart = request.POST['cart']
			items = request.POST['items']
			email = request.POST['email']
			address = request.POST['address']

			data = Cart.objects.filter(cart_id=cart, status='').update(status='paid')
			new_shipment = Shipment.objects.create(order=order, address=address, items=items, status='', user=request.user)
			new_shipment.save()
			carts = Cart.objects.filter(cart_id=request.session['id'], status="")
			for product in carts:
				sel_prod = Product.objects.get(product.prodid)
				sel_prod.quantity -= product.quantity
				sel_prod.save()

			return HttpResponse(data)
