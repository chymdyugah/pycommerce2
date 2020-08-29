from django.shortcuts import render, redirect
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
import random
from pycommerce.settings import LOGIN_REDIRECT_URL
from .models import Product, Cart
from .forms import LoginForm, RegistrationForm
from django.db.models import Sum

# Create your views here.


class Index(generic.ListView):
	template_name = 'irish/index2.html'

	def get(self, request, *args, **kwargs):
		if not request.session.has_key('id'):
			request.session['id'] = random.randint(999, 9999999)

		products = Product.objects.all()
		cart = Cart.objects.filter(cart_id=request.session['id'], status='').count()
		pet = request.session['id']
		return render(request, self.template_name, {'products': products, 'cart': cart, 'pet': pet})


class CartView(generic.ListView):
	template_name = 'irish/cart2.html'

	def get(self, request, *args, **kwargs):
		if not request.session.has_key('id'):
			request.session['id'] = random.randint(999, 9999999)

		pet = request.session['id']
		products = Cart.objects.filter(cart_id=request.session['id'], status="")
		cart = Cart.objects.filter(cart_id=request.session['id'], status="").count()
		subtotal = Cart.objects.filter(cart_id=request.session['id'], status="").aggregate(Sum('total'))
		subtotal = subtotal['total__sum']
		if subtotal is None:
			subtotal = ""
		final = ""
		for product in products:
			final += product.prod_name+","+str(product.quantity)+";"

		return render(request, self.template_name, {'cart': cart, 'products': products, 'subtotal': subtotal, 'final': final, 'pet': pet})


@method_decorator(login_required, name='dispatch')
class Checkout(View):
	template_name = 'irish/checkout2.html'

	def get(self, request):
		if not request.session.has_key('id'):
			request.session['id'] = random.randint(999, 9999999)

		pet = request.session['id']
		products = Cart.objects.filter(cart_id=request.session['id'], status="")
		cart = Cart.objects.filter(cart_id=request.session['id'], status="").count()
		subtotal = Cart.objects.filter(cart_id=request.session['id'], status="").aggregate(Sum('total'))
		subtotal = subtotal['total__sum']
		if subtotal is None:
			subtotal = ""
		final = ""
		for product in products:
			final += product.prod_name + "," + str(product.quantity) + ";"

		return render(request, self.template_name, {'cart': cart, 'products': products, 'subtotal': subtotal, 'final': final, 'pet': pet})


class Single(generic.DetailView):
	template_name = 'irish/single1.html'
	model = Product

	def get(self, request, pk, *args, **kwargs):
		if not request.session.has_key('id'):
			request.session['id'] = random.randint(999, 9999999)
		try:
			prod = Product.objects.get(pk=pk)
		except Product.DoesNotExist:
			return redirect('irish:index')

		cart = Cart.objects.filter(cart_id=request.session['id'], status="").count()
		pet = request.session['id']
		return render(request, self.template_name, {'product': prod, 'cart': cart, 'pet': pet})


class Login(View):
	template_name = 'irish/login.html'
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

			res = 'Wrong Username or Password'
		return render(request, self.template_name, {'form': form, 'res': res})


class Registration(View):
	template_name = 'irish/register.html'
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


class Logout(LogoutView):
	next_page = "irish:index"

	def get(self, request, *args, **kwargs):
		Cart.objects.filter(cart_id=request.session['id'], status='').delete()
		return super().get(request)


class LogoutV(View):
	def get(self, request):
		Cart.objects.filter(cart_id=request.session['id'], status='').delete()
		logout(request)
		return redirect('irish:index')


# ajax view
class AjxView(View):

	def get(self, request):
		if 'quant' in request.GET:
			pid = request.GET['serial']
			quant = int(request.GET['quant'])
			product = Cart.objects.get(pk=pid)
			sel_prod = Product.objects.get(pk=product.prodid)
			price = sel_prod.price
			total = price * quant
			product.quantity = quant
			product.total = total
			product.save()

			return HttpResponse(total)

		if "sn" in request.GET:
			pid = request.GET['sn']
			Cart.objects.get(pk=pid).delete()

			return HttpResponse('done')

	def post(self, request):
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

		if 'up' in request.POST:
			order = request.POST['order']
			cart = request.POST['cart']
			items = request.POST['items']
			email = request.POST['email']
			address = request.POST['address']

			data = Cart.objects.filter(cart_id=cart, status='').update(status='paid')
			return HttpResponse(data)
