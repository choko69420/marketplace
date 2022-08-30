from django.shortcuts import render, redirect
#import models
from .models import Inventory, Sales
from .forms import InventoryForm, SalesForm


def index(request):
    # create a dictionary to pass to the template engine as its context
    # key will be the name of the field in the template
    # value will be the data for that field
    context = {
        'inventory': Inventory.objects.all().values(),
        'sales': Sales.objects.all().values(),
    }
    return render(request, 'inventorymanagment/index.html', context)


def add_sales(request):
    # if method is GET
    if request.method == 'GET':
        # create a form instance and pass it to the template
        form = SalesForm()
        return render(request, 'inventorymanagment/sales.html', {'form': form})
    # if method is POST
    # create a form instance and populate it with data from the request
    form = SalesForm(request.POST)
    if form.is_valid():
        # process the data in form.cleaned_data as required
        # save
        form.save()
        # record sale in inventory
        item = form.cleaned_data.get('item')
        quantity = form.cleaned_data.get('quantity')
        item.remaining -= quantity
        item.sold += quantity
        item.save()
        # redirect to home page
        return redirect('/')
    # if form is invalid
    else:
        # return an error message
        return render(request, 'inventorymanagment/sales.html', {'form': form})


def add_inventory(request):
    # if method is GET
    if request.method == 'GET':
        # create a form instance and pass it to the template
        form = InventoryForm()
        return render(request, 'inventorymanagment/inventory.html', {'form': form})
    # if method is POST
    else:
        # create a form instance and populate it with data from the request
        # (binding)
        form = InventoryForm(request.POST)
        # check whether it's valid
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # save
            form.save()
            # redirect to home page
            return redirect('/')
        # if form is invalid
        else:
            # return an error message
            return render(request, 'inventorymanagment/inventory.html', {'form': form})
