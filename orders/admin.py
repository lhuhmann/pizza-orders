from django.contrib import admin

# Register your models here.
from .models import *

print(type(Customer))

tables = [Item, ToppingType, Topping, ItemTopping, Customer, Order, OrderItem, OrderItemTopping]
for table in tables:
    admin.site.register(table)
