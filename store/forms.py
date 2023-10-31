from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Customer, ShippingAddress, Order, Product
from django.utils.translation import gettext_lazy as _

class CreateCustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
        labels = {
            'username': _('Account Username'),
            'first_name': _('Name'),
            'email': _('Email ID'),
        }

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']
        labels = {
            'name': _('Name'),
            'email': _('Email Address'),
        }

class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'zipcode', 'receipt']
        labels = {
            'address': _('Delivery Address'),
            'city': _('City'),
            'state': _('State'),
            'zipcode': _('6 Digit PIN Code'),
            'receipt': _('Upload Payment Confirmation Screenshot'),
        }

class OrderStatusForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        labels = {
            'status': _('Update Order Status'),
        }

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'name': _('Name'),
            'price': _('Price'),
            'category': _('Category'),
            'colour': _('Colour'),
            'size': _('Size'),
            'fabric': _('Fabric'),
            'image': _('Image'),
            'instock': _('In Stock?')
        }