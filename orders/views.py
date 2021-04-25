import sys

from django import forms
from django.shortcuts import render
from django.http import HttpResponse

from .models import Item, ItemTypeTopping

# Forms
class OrderForm(forms.Form):
    toppings_choices = (
        ("t1", "cheese"),
        ("t2", "arugula"),
        ("t3", "olives"),
    )
    toppings = forms.MultipleChoiceField(choices=toppings_choices, widget=forms.CheckboxSelectMultiple)

    def clean_toppings(self):
        print(self.cleaned_data, file=sys.stderr)
        value = self.cleaned_data['toppings']
        if len(value) > 2:
            raise forms.ValidationError("You can't select more than 2 items.")
        return value

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

def add_item(request, item_id):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            data = order_form.cleaned_data
    else:
        order_form = OrderForm()
    return render(request, "orders/add_item.html", {
        "item": Item.objects.filter(id = item_id),
        "order_form": order_form
    })
