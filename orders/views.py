import sys

from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import Customer, Item, ItemTypeTopping, ToppingType, Order, OrderItem, OrderItemTopping, Topping

### Forms
# class OrderForm(forms.Form):
#     toppings_test = ItemTypeTopping.objects.filter()
#     toppings_choices = (
#         ('t1', 'cheese'),
#         ('t2', 'arugula'),
#         ('t3', 'olives'),
#     )
#     toppings = forms.MultipleChoiceField(choices=toppings_choices, widget=forms.CheckboxSelectMultiple)

#     def clean_toppings(self):
#         print(self.cleaned_data, file=sys.stderr)
#         value = self.cleaned_data['toppings']
#         if len(value) > 2:
#             raise forms.ValidationError('You can't select more than 2 items.')
#         return value
# Do not use a ModelForm here because it assumes you want to create a user and validation will fail
# with the error that this user already exists
class LoginForm(forms.Form):
    user = forms.CharField(label='Username', max_length=64)
    # instead of using the default widget, use password widget
    password = forms.CharField(widget=forms.PasswordInput())

class RegistrationForm(forms.ModelForm):
    # TODO: Ideally I should have the validate password field also inherit its characteristics from the Customer model
    password2 = forms.CharField(max_length=64, label='Confirm password')

    class Meta:
        model = Customer
        # writing out the fields rather than using fields = '__all__' because I want the password last, next to the confirm password field
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        # Because of associating this form with the 'Customer' model, Django already ensures no duplicate usernames exist
        # ensure that passwords match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError(
                    'Registration failed - passwords do not match'
                )

### Views
def index(request):
    return render(request, 'orders/base.html')

def greet(request, name):
    return HttpResponse(f'Hello, {name.capitalize()}')

def login(request):
    '''Log in user'''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            password = form.cleaned_data['password']
            # check if that (username, password) pair exist in the db
            customer = Customer.objects.filter(username=user, password=password)
            if customer:
                request.session['username'] = user
                return redirect('menu')
            else:
                login_error = 'The submitted username or password is incorrect'
                return render(request, 'orders/login.html', {
                    'form': form,
                    'login_error': login_error
                })
    else:
        form = LoginForm()
        return render(request, 'orders/login.html', {'form': form})

def logout(request):
    '''Log out user'''
    try:
        del request.session['username']
    except KeyError:
        pass
    return render(request, 'orders/login.html', {
        'logout': 'Logout successful',
        'form': LoginForm()
        })

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'orders/register.html', {'form': form})

def menu(request):
    if not 'username' in request.session:
        return render(request, 'orders/login.html', {
            'form': LoginForm(),
            'login_error': 'You must log in to access the menu'
        })
    else:
        # TODO: I think ideally pull all the distinct menu types and iterate over them rather than hard-coding them?
        return render(request, 'orders/menu.html', {
            'menus': {
            'reg_pizza': Item.objects.filter(menu = 'Regular Pizza'),
            'sicilian_pizza': Item.objects.filter(menu = 'Sicilian Pizza'),
            'sub': Item.objects.filter(menu = 'Subs'),
            'pasta': Item.objects.filter(menu = 'Pasta'),
            'salad': Item.objects.filter(menu = 'Salads'),
            'dinner_platter': Item.objects.filter(menu = 'Dinner Platters')
            }
        })

def add_to_cart(request, quantity, item, toppings, topping_num = None, topping_ids = None):
    customer = Customer.objects.get(username = request.session['username'])
    # create a cart for this user if they don't have one
    if not Order.objects.filter(customer = customer, status = "Cart").exists():
        order = Order.objects.create(customer = customer, status = "Cart")
        order.save()
    else:
        order = Order.objects.get(customer = customer, status = "Cart")
    for i in range(quantity):
        # add each ordered item to OrderItem table
        order_item = OrderItem.objects.create(order = order, item = item)
        order_item.save()
        if toppings:
            # add each item-topping pair to OrderItemTopping table
            for i in range(topping_num):
                topping_id = topping_ids[i]
                topping_name = ItemTypeTopping.objects.get(id = topping_id).topping
                topping = Topping.objects.get(topping = topping_name)
                # print(item_type_topping, file=sys.stderr)
                # raise NameError()
                order_item_topping = OrderItemTopping.objects.create(order_item = order_item, topping = topping)
                order_item_topping.save()


def add_item(request, item_id):
    if not 'username' in request.session:
        return render(request, 'orders/login.html', {
            'form': LoginForm(),
            'login_error': 'You must log in to add an item'
        })
    else:
        if request.method == 'POST':
            data = request.POST
            item_id = data['item']
            item = Item.objects.filter(id = item_id).first()
            topping_num = int(data['topping_num'])
            quantity = int(data['quantity'])
            if topping_num > 0:
                # It's necessary to use getlist here, since using the key directly as above
                # only returns the last value if there are multiple values associated with the key.
                topping_ids = request.POST.getlist('topping')
                # topping_ids may be either string or list of strings
                # want a consistent format, so convert to list of ints
                if isinstance(topping_ids, str):
                    topping_ids = [int(topping_ids)]
                else:
                    topping_ids = list(map(int, topping_ids))
                if len(topping_ids) > topping_num:
                    toppings_error = f'The maximum number of toppings permitted for this item is {topping_num}.'
                    return render(request, 'orders/add_item.html', {
                    'item': item,
                    'topping_choices': ItemTypeTopping.objects.filter(item_type = item.item_type),
                    'topping_ids': topping_ids,
                    'topping_num': ToppingType.objects.filter(topping_type = item.topping_type).first().topping_num,
                    'toppings_error': toppings_error,
                    'quantity': quantity
                    })
                elif len(topping_ids) < topping_num:
                    toppings_error = f'Insufficient toppings selected.'
                    return render(request, 'orders/add_item.html', {
                    'item': item,
                    'topping_choices': ItemTypeTopping.objects.filter(item_type = item.item_type),
                    'topping_ids': topping_ids,
                    'topping_num': ToppingType.objects.filter(topping_type = item.topping_type).first().topping_num,
                    'toppings_error': toppings_error,
                    'quantity': quantity
                    })
                else:
                    add_to_cart(request = request, quantity = quantity, item = item, toppings = True)
                    return HttpResponseRedirect(reverse('cart'))
            else:
                add_to_cart(request = request, quantity = quantity, item = item, toppings = False)
                return HttpResponseRedirect(reverse('cart'))
        else:
            # order_form = OrderForm()
            item = Item.objects.filter(id = item_id).first()
            return render(request, 'orders/add_item.html', {
                'item': item,
                'topping_choices': ItemTypeTopping.objects.filter(item_type = item.item_type),
                'topping_num': ToppingType.objects.filter(topping_type = item.topping_type).first().topping_num
        })

def cart(request):
    return render(request, 'orders/cart.html', {
    'item': "hello"
    })

