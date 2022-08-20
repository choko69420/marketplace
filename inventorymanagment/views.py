from django.shortcuts import render

#import models
from .models import Inventory, Sales


def index(request):
    # create a dictionary to pass to the template engine as its context
    # key will be the name of the field in the template
    # value will be the data for that field
    context = {
        'inventory': [i.as_dict() for i in Inventory.objects.all()],
    }
    return render(request, 'inventorymanagment/index.html', context)
