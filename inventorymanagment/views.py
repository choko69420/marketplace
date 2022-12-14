from django.shortcuts import render, redirect
from .models import Inventory, Sales
from .forms import InventoryForm, SalesForm, LoginForm, DeleteSalesForm, DeleteInventoryForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class indexView(ListView):
    model = Inventory
    template_name = 'inventorymanagment/index.html'
    context_object_name = 'inventory, sales'
    ordering = ['-id']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales'] = Sales.objects.all().values()
        # turn context item_id into item name
        for sale in context['sales']:
            sale['item_id'] = Inventory.objects.get(id=sale['item_id']).name
        # change item_id key into item name key
        context['sales'] = [{'id': sale['id'], 'item_name': sale['item_id'], 'quantity': sale['quantity'],
                             'day': sale['day']} for sale in context['sales']]
        context['inventory'] = Inventory.objects.all().values()
        return context


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


def delete_sales(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        form = DeleteSalesForm()
        print("GET")
        return render(request, 'inventorymanagment/delete_sales.html', {'form': form})
    form = DeleteSalesForm(request.POST)
    if form.is_valid():
        form.delete_sale()
        # redirect
        return redirect('/')
    else:
        return render(request, 'inventorymanagment/delete_sales.html', {'form': form})


def delete_inventory(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        form = DeleteInventoryForm()
        return render(request, 'inventorymanagment/delete_inventory.html', {'form': form})
    form = DeleteInventoryForm(request.POST)
    if form.is_valid():
        id = form.cleaned_data.get('id')
        item = Inventory.objects.get(id=id)
        item.delete()
        # redirect
        return redirect('/')
    else:
        return render(request, 'inventorymanagment/delete_inventory.html', {'form': form})


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
    # handle login


def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'inventorymanagment/login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'inventorymanagment/login.html', {'form': form, 'error': 'Invalid credentials'})
        else:
            return render(request, 'inventorymanagment/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')
