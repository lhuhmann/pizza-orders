from django.shortcuts import render
from django.http import HttpResponse

from .models import Item

# Create your views here.
def index(request):
    return render(request, "orders/base.html")

def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}")

def menu(request):
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
