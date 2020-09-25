from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import RegistrationForm, LoginForm
from .models import Refill
from irish.models import Product, Cart, Shipment
from django.db.models import Sum
import datetime
import re


# Create your views here.
class Login(generic.View):
	template_name = 'adumin/login.html'
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
				if user.is_staff:
					login(request, user)
					if 'next' in request.GET:
						return redirect(request.GET['next'])
					else:
						return redirect('adumin:index')

		err = "Invalid username or Password"
		return render(request, self.template_name, {'form': form, 'err': err})


class Logout(generic.View):
	def get(self, request):
		logout(request)
		return redirect('adumin:login')


class Registration(generic.View):
	template_name = 'adumin/register.html'
	form_class = RegistrationForm

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.form_class(request.POST)
		regex = re.compile('/\W+/')

		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']

			# validate the username, fname and lname to check if they contain characters that is not alphanumeric or _
			if regex.search(username) or regex.search(first_name) or regex.search(last_name) is not None:
				err = "Do not include any non word characters"
				return render(request, self.template_name, {'form': form, 'err': err})

			user.set_password(password)
			user.is_staff = True  # only staffs are allowed to login
			user.save()

			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('adumin:index')

		return render(request, self.template_name, {'form': form})


@method_decorator(login_required(login_url='/adumin/login/'), name='dispatch')
class Index(generic.View):
	template_name = 'adumin/index.html'

	def get(self, request):
		if not request.user.is_staff:
			return redirect('adumin:logout')

		datediff = datetime.date.today() - datetime.timedelta(3)
		active_carts = Cart.objects.filter(date__gt=datediff, status='').count()
		stalled_carts = Cart.objects.filter(date__lte=datediff, status='').count()
		shipments = Shipment.objects.filter(status='').count()

		sales = Cart.objects.filter(status='paid').values('prod_name').annotate(quant=Sum('quantity'))
		prods = Product.objects.values('name').annotate(quant=Sum('quantity'))

		return render(request, self.template_name, {'act': active_carts, 'stall': stalled_carts, 'shipments': shipments, 'prods': prods, 'sales': sales})


@method_decorator(login_required(login_url='/adumin/login/'), name='dispatch',)
class Inventory(generic.View):
	template_name = 'adumin/inventory.html'

	def get(self, request):
		if not request.user.is_staff:
			return redirect('adumin:logout')

		stocks = Product.objects.all()
		refills = Refill.objects.all()
		return render(request, self.template_name, {'stocks': stocks, 'refills': refills})


@method_decorator(login_required(login_url='/adumin/login/'), name='dispatch',)
class RefillView(generic.View):
	template_name = 'adumin/refill.html'

	def get(self, request):
		if not request.user.is_staff:
			return redirect('adumin:logout')

		products = Product.objects.all()
		inventory = Product.objects.values('name').annotate(quant=Sum('quantity'))
		return render(request, self.template_name, {'products': products, 'inventory': inventory})

	def post(self, request):
		if 'newproduct' in request.POST:
			name = request.POST['name']
			price = request.POST['price']
			description = request.POST['desc']
			categories = request.POST['tag']
			image = request.FILES['image']
			prodid = 'prod' + str(hash(datetime.datetime.now()))

			new_product = Product.objects.create(prodid=prodid, name=name, price=price, description=description, categories=categories, image=image)
			new_product.save()
			return self.get(request)

		if 'submit' in request.POST:
			product = request.POST['product']
			quantity = request.POST['quantity']

			sel_product = Product.objects.get(prodid=product)
			sel_product.quantity += int(quantity)
			sel_product.save()
			new_refill = Refill.objects.create(product=sel_product, quantity=int(quantity))
			new_refill.save()
			return self.get(request)


@method_decorator(login_required(login_url='/adumin/login/'), name='dispatch',)
class Redr(generic.View):
	template_name = 'adumin/redr.html'

	def get(self, request):
		if not request.user.is_staff:
			return redirect('adumin:logout')

		datediff = datetime.date.today() - datetime.timedelta(3)
		stalled_carts = Cart.objects.filter(date__lte=datediff, status='').values('cart_id').annotate(totall=Sum('total'))
		carts = Cart.objects.all()
		shipments = Shipment.objects.all()
		return render(request, self.template_name, {'stall': stalled_carts, 'orders': carts, 'shipments': shipments})


@method_decorator(login_required(login_url='/adumin/login/'), name='dispatch',)
class InventCharts(generic.View):
	template_name = 'adumin/inventcharts.html'

	def get(self, request):
		if not request.user.is_staff:
			return redirect('adumin:logout')

		sales = Cart.objects.filter(status='paid').values('prod_name').annotate(quant=Sum('quantity'))
		return render(request, self.template_name, {'sales': sales})


class Ajx(generic.View):
	def get(self, request):
		# mark an order as shipped
		if 'q' in request.GET:
			try:
				shipment = Shipment.objects.get(pk=request.GET['q'])
			except Shipment.DoesNotExist:
				return HttpResponse("<script>location.replace('/adumin/redr/')</script>")
			else:
				shipment.status = "shipped"
				shipment.save()
				return HttpResponse("<script>location.replace('/adumin/redr/')</script>")

	def post(self, request):
		# select date range and send back products sold during that range
		if 'dat1' in request.POST:
			dat1 = request.POST['dat1']
			dat2 = request.POST['dat2']
			selection = Cart.objects.filter(status='paid', date__gte=dat1, date__lte=dat2).values('prod_name').annotate(quant=Sum('quantity'))
			response = [{'prod_name': prod['prod_name'], 'quant': prod['quant']} for prod in selection]
			return JsonResponse(response, safe=False)
