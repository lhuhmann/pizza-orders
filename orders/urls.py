from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('name/<str:name>', views.greet, name='greet'),
    path('menu/', views.menu, name='menu'),
    path('add_item/<int:item_id>/', views.add_item, name='add_item')
]
