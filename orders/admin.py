from django.contrib import admin

# Register your models here.
from .models import *

print(type(Customer))

tables = [ToppingType, Topping, Item, ItemTypeTopping, Customer, Order, OrderItem, OrderItemTopping]
for table in tables:
    admin.site.register(table)
