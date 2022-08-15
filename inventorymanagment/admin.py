from django.contrib import admin

# Register your models here.
from inventorymanagment.models import Inventory, Sales
# register all models
admin.site.register(Inventory)
admin.site.register(Sales)
