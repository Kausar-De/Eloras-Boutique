from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True, blank=True)
	email = models.CharField(max_length=200, null=True, blank=True)
	device = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		if self.name:
			name = self.name
		else:
			name = self.device
		return str(name)


class Product(models.Model):
    CATEGORIES = (
        ('Saree', 'Saree'),
        ('Salwar Kameez', 'Salwar Kameez'),
        ('Leggings', 'Leggings'),
        ('Nightie', 'Nightie'),
        ('Blouse Piece', 'Blouse Piece'),
        ('Top', 'Top'),
        ('Kurti', 'Kurti'),
    )

    COLOURS = (
        ('Orange', 'Orange'),
        ('Brown', 'Brown'),
        ('Black', 'Black'),
        ('Green', 'Green'),
        ('Blue', 'Blue'),
        ('Pink', 'Pink'),
        ('Red', 'Red'),
        ('Yellow', 'Yellow'),
        ('Gray', 'Gray'),
        ('White', 'White'),
    )

    SIZES = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('U', 'U'),
    )

    FABRICS = (
        ('Silk', 'Silk'),
        ('Cotton', 'Cotton'),
    )

    name = models.CharField(max_length = 200, null = True)
    price = models.DecimalField(max_digits = 9, decimal_places = 2)
    category = models.CharField(max_length = 200, choices = CATEGORIES, default = 'Choose Category...')
    colour = models.CharField(max_length = 200, choices = COLOURS, default = 'Choose Colour...')
    size = models.CharField(max_length = 200, choices = SIZES, default = 'Choose Size...')
    fabric = models.CharField(max_length = 200, choices = FABRICS, default = 'Choose Fabric...')
    image = models.ImageField(default = '/placeholder.png', null = True, blank = True)
    instock = models.BooleanField(default = True, null = True, blank = False)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default = False)
    txn_id = models.CharField(max_length = 200, null = True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.product.price for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = len(orderitems)
        return total

    @property
    def get_cart_details(self):
        orderitems = self.orderitem_set.all()
        products = [item.product for item in orderitems]
        return products

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	date_added = models.DateTimeField(auto_now_add=True)
        
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    receipt = models.ImageField(default = '/receipts/placeholder.png', upload_to = 'receipts', null = False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address 