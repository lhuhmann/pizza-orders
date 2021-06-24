from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('name/<str:name>', views.greet, name='greet'),
    path('menu', views.menu, name='menu'),
    path('add_item/<int:item_id>/', views.add_item, name='add_item'),
    path('cart', views.cart, name='cart'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register')
]
