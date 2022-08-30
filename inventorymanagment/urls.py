from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_sales', views.add_sales, name='create_sales'),
    path('add_inventory', views.add_inventory, name='add_inventory'),
]
