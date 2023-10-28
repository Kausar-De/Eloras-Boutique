import django_filters
from django_filters import RangeFilter, MultipleChoiceFilter, widgets
from .models import *
from django import forms

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

class MyRangeWidget(django_filters.widgets.RangeWidget):
    
    def __init__(self, from_attrs = None, to_attrs = None, attrs = None):
        super(MyRangeWidget, self).__init__(attrs)
        if from_attrs:
            self.widgets[0].attrs.update(from_attrs)
        if to_attrs:
            self.widgets[1].attrs.update(to_attrs)

class ProductFilter(django_filters.FilterSet):
    category = MultipleChoiceFilter(field_name = 'category', choices = CATEGORIES, label = 'Category', widget = forms.CheckboxSelectMultiple())
    colour = MultipleChoiceFilter(field_name = 'colour', choices = COLOURS, label = 'Colour', widget = forms.CheckboxSelectMultiple())
    size = MultipleChoiceFilter(field_name = 'size', choices = SIZES, label = 'Size', widget = forms.CheckboxSelectMultiple())
    fabric = MultipleChoiceFilter(field_name = 'fabric', choices = FABRICS, label = 'Fabric', widget = forms.CheckboxSelectMultiple())
    price = RangeFilter(field_name = 'price', label = 'Price Range', widget = MyRangeWidget(from_attrs={'placeholder':'Minimum'}, to_attrs={'placeholder':'Maximum'},))
    class Meta:
        model = Product
        exclude = ['name', 'image', 'instock', 'price', 'category', 'colour', 'size', 'fabric']