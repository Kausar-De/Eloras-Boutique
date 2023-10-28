from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
import datetime
from .forms import CreateCustomerForm, CustomerForm, ShippingAddressForm
from .models import *
from .filters import ProductFilter
# Create your views here.

"""def homepage(request):
	try:
		try:
			customer = request.user.customer	
		except:
			device = request.COOKIES['device']
			customer, created = Customer.objects.get_or_create(device = device)
		order, created = Order.objects.get_or_create(customer = customer, complete = False)
		cartItems = order.get_cart_items	
	except:
		cartItems = 0

	context = {'cartItems':cartItems}
	return render(request, 'store/homepage.html', context)"""

def store(request):
	products = Product.objects.all()
	myFilter = ProductFilter(request.GET, queryset = products)
	products = myFilter.qs

	try:
		try:
			customer = request.user.customer	
		except:
			device = request.COOKIES['device']
			customer, created = Customer.objects.get_or_create(device = device)
		order, created = Order.objects.get_or_create(customer = customer, complete = False)
		cartItems = order.get_cart_items	
	except:
		cartItems = 0
    
	context = {'products':products, 'myFilter':myFilter, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def product(request, pk):
	try:
		customer = request.user.customer	
	except:
		device = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(device = device)

	product = Product.objects.get(id = pk)
	order, created = Order.objects.get_or_create(customer=customer, complete = False)

	if request.method == 'POST':
		orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
		orderItem.save()
		messages.info(request, 'Item Added to Cart Successfully!')
		return redirect('store')
	
	cartItems = order.get_cart_items

	context = {'product':product, 'cartItems':cartItems}
	return render(request, 'store/product.html', context)

def cart(request):
	try:
		customer = request.user.customer
	except:
		device = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(device = device)

	order, created = Order.objects.get_or_create(customer = customer, complete = False)
	cartItems = order.get_cart_items

	context = {'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def removeItem(request, pk):
	orderitem = OrderItem.objects.get(id = pk)

	orderitem.delete()

	messages.info(request, 'Item Removed from Cart Successfully!')
    
	return redirect('cart')

def checkout(request):
	try:
		customer = request.user.customer
	except:
		device = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(device = device)

	order, created = Order.objects.get_or_create(customer = customer, complete = False)
	cartItems = order.get_cart_items

	txn_id = datetime.datetime.now().timestamp()
	order.txn_id = txn_id
	
	shippingform = ShippingAddressForm(request.POST, request.FILES)

	if customer.user == None:
		custform = CustomerForm(request.POST)
		if request.method == 'POST':
			custform = CustomerForm(request.POST)
			shippingform = ShippingAddressForm(request.POST, request.FILES)
			if custform.is_valid() and shippingform.is_valid():
				order.date_ordered = timezone.now()
				order.complete = True
				order.save()

				customer.name = custform.cleaned_data.get('name')
				customer.email = custform.cleaned_data.get('email')

				ship = shippingform.save(commit = False)
				ship.customer = customer
				ship.order = order
				ship.save()

				custname = custform.cleaned_data.get('name')
				template = get_template("store/emailtemplate.html")
				mailbody = template.render({'order':order, 'cartItems':cartItems, 'shippingform':shippingform, 'custname': custname})
				email = EmailMessage(
					subject = "Elora's Boutique - Order Placed Successfully!",
					body = mailbody,
					from_email = settings.EMAIL_HOST_USER,
					to = [custform.cleaned_data.get('email'), 'de_elora1@hotmail.com'],
				)
				email.content_subtype = "html"
				email.send()	

				messages.info(request, 'Order Placed! You will receive communication via email!')
				return redirect('store')
		context = {'order':order, 'cartItems':cartItems, 'custform':custform, 'shippingform':shippingform}
	else:
		if request.method == 'POST':
			shippingform = ShippingAddressForm(request.POST, request.FILES)
			if shippingform.is_valid():
				order.date_ordered = timezone.now()
				order.complete = True
				order.save()				
				
				ship = shippingform.save(commit = False)
				ship.customer = customer
				ship.order = order
				ship.save()

				custname = request.user.customer.name
				template = get_template("store/emailtemplate.html")
				mailbody = template.render({'order':order, 'cartItems':cartItems, 'shippingform':shippingform, 'custname': custname})
				email = EmailMessage(
					subject = "Elora's Boutique - Order Placed Successfully!",
					body = mailbody,
					from_email = settings.EMAIL_HOST_USER,
					to = [request.user.customer.email, 'de_elora1@hotmail.com'],
				)
				email.content_subtype = "html"
				email.send()				

				messages.info(request, 'Order Placed! You will receive communication via email! Visit "My Orders" for details.')
				return redirect('store')
		context = {'order':order, 'cartItems':cartItems, 'shippingform':shippingform}
	
	return render(request, 'store/checkout.html', context)

def loginPage(request):
	try:
		customer = request.user.customer
	except:
		device = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(device = device)

	order, created = Order.objects.get_or_create(customer = customer, complete = False)
	cartItems = order.get_cart_items

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username = username, password = password)

		if user is not None:
			login(request, user)
			return redirect('store')
		else:
			messages.info(request, 'Username OR Password is incorrect!')
			return render(request, 'store/login.html')

	context = {'cartItems':cartItems}

	return render(request, 'store/login.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'Successfully logged out!')
    return redirect('login')

def registerPage(request):
	try:
		customer = request.user.customer
	except:
		device = request.COOKIES['device']
		customer, created = Customer.objects.get_or_create(device = device)

	order, created = Order.objects.get_or_create(customer = customer, complete = False)
	cartItems = order.get_cart_items

	form = CreateCustomerForm
    
	if request.method == 'POST':
		form = CreateCustomerForm(request.POST)
		if form.is_valid():
			form.save()
			uname = form.cleaned_data.get('username')
			user = User.objects.get(username = uname)
			name = form.cleaned_data.get('first_name')
			email = form.cleaned_data.get('email')
			customer, created = Customer.objects.get_or_create(user = user, name = name, email = email)
			customer.save()
			messages.success(request, name + ' was registered successfully!')
			return redirect('login')

	context = {'form':form, 'cartItems':cartItems}

	return render(request, 'store/register.html', context)

def myOrders(request):
	customer = request.user.customer
	orders = Order.objects.filter(customer = customer, complete = True).order_by('-date_ordered')

	order, created = Order.objects.get_or_create(customer = customer, complete=False)
	cartItems = order.get_cart_items

	context = {'orders':orders, 'cartItems':cartItems}

	return render(request, 'store/myorders.html', context)

def emailtemplate(request):
	return render(request, 'store/emailtemplate.html')