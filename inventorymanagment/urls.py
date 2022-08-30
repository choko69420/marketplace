from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_sales', views.add_sales, name='add_sale'),
    path('add_inventory', views.add_inventory, name='add_inventory'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('delete_sales', views.delete_sales, name='delete_sale'),
    path('delete_inventory', views.delete_inventory, name='delete_inventory'),
]
