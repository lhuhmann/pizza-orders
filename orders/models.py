from django.db import models
from django.db.models.fields.related import ForeignKey

class ToppingEnum(models.TextChoices):
    cheese = 'Cheese'
    one = '1 topping'
    two = '2 toppings'
    three = '3 toppings'
    special = 'Special'

### Foods ###
# defines number of toppings for each topping type
class ToppingType(models.Model):
    # enumerate field
    class ToppingNumEnum(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2

    # data columns
    topping_type = models.CharField(
        max_length=64,
        primary_key = True
        )
    topping_num = models.IntegerField(choices=ToppingNumEnum.choices)

# list of all toppings
class Topping(models.Model):
    topping = models.CharField(max_length=64, primary_key=True)

class Item(models.Model):
    # enumerate fields
    class MenuEnum(models.TextChoices):
        regular_pizza = 'Regular Pizza'
        sicilian_pizza = 'Sicilian Pizza'
        subs = 'Subs'
        pasta = 'Pasta'
        salads = 'Salads'
        dinner_platters = 'Dinner Platters'

    class SizeEnum(models.TextChoices):
        small = 'Small'
        large = 'Large'

    # data columns
    item_type = models.CharField(max_length=64)
    menu = models.CharField(
        max_length=64,
        choices = MenuEnum.choices
        )
    topping_type = models.ForeignKey(
        ToppingType,
        on_delete=models.CASCADE,
        null = True
        )
    size = models.CharField(
        max_length=64,
        choices = SizeEnum.choices
        )
    price = models.DecimalField(max_digits=8, decimal_places=2)

# defines which item type(s) each topping can be paired with
class ItemTypeTopping(models.Model):
    item_type = models.CharField(max_length=64)
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

### Orders ###
class Customer(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

class Order(models.Model):
    # enumerate field
    class StatusEnum(models.TextChoices):
        ordered = "Ordered"
        cart = "Cart"

    # columns
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=64,
        choices = StatusEnum.choices
        )

class OrderItem(models.Model):
    order_id =  models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

class OrderItemTopping(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
