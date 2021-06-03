import sys

from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Item, ItemTypeTopping, ToppingType

# Forms
# class OrderForm(forms.Form):
#     toppings_test = ItemTypeTopping.objects.filter()
#     toppings_choices = (
#         ("t1", "cheese"),
#         ("t2", "arugula"),
#         ("t3", "olives"),
#     )
#     toppings = forms.MultipleChoiceField(choices=toppings_choices, widget=forms.CheckboxSelectMultiple)

#     def clean_toppings(self):
#         print(self.cleaned_data, file=sys.stderr)
#         value = self.cleaned_data['toppings']
#         if len(value) > 2:
#             raise forms.ValidationError("You can't select more than 2 items.")
#         return value

# Create your views here.
def index(request):
    return render(request, "orders/base.html")

def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}")

def menu(request):
    # TODO: I think ideally pull all the distinct menu types and iterate over them rather than hard-coding them?
    return render(request, "orders/menu.html", {
        "menus": {
        "reg_pizza": Item.objects.filter(menu = "Regular Pizza"),
        "sicilian_pizza": Item.objects.filter(menu = "Sicilian Pizza"),
        "sub": Item.objects.filter(menu = "Subs"),
        "pasta": Item.objects.filter(menu = "Pasta"),
        "salad": Item.objects.filter(menu = "Salads"),
        "dinner_platter": Item.objects.filter(menu = "Dinner Platters")
        }
    })

def validate_toppings(topping_num, toppings):
    if len(toppings) > topping_num:
        return False
    else:
        return True

def add_item(request, item_id):
    if request.method == "POST":
        data = request.POST
        print("data", file=sys.stderr)
        print(data, file=sys.stderr)
        item_id = data["item"]
        item = Item.objects.filter(id = item_id).first()
        topping_num = int(data["topping_num"])
        quantity = data["quantity"]
        if "topping" in data:
            # It's necessary to use getlist here, since using the key directly as above
            # only returns the last value if there are multiple values associated with the key.
            topping_ids = request.POST.getlist("topping")
            # topping_ids may be either string or list of strings
            # want a consistent format, so convert to list of ints
            if isinstance(topping_ids, str):
                topping_ids = [int(topping_ids)]
            else:
                topping_ids = list(map(int, topping_ids))
            toppings_are_valid = validate_toppings(topping_num, topping_ids)
        # order_form = OrderForm(request.POST)
        # if order_form.is_valid():
            # data = order_form.cleaned_data
        # redirect user to menu page (probably not exactly what we want)
        if toppings_are_valid:
            return HttpResponseRedirect(reverse("menu"))
        else:
            toppings_error = f'The maximum number of toppings permitted for this item is {topping_num}.'
            return render(request, "orders/add_item.html", {
            "item": item,
            "topping_choices": ItemTypeTopping.objects.filter(item_type = item.item_type),
            "topping_num": ToppingType.objects.filter(topping_type = item.topping_type).first().topping_num,
            "toppings_error": toppings_error,
            "quantity": quantity
    })
    else:
        # order_form = OrderForm()
        item = Item.objects.filter(id = item_id).first()
        return render(request, "orders/add_item.html", {
            "item": item,
            "topping_choices": ItemTypeTopping.objects.filter(item_type = item.item_type),
            "topping_num": ToppingType.objects.filter(topping_type = item.topping_type).first().topping_num
    })
