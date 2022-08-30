# make boilerplate forms
from django import forms
from django.forms import ModelForm
from .models import Inventory, Sales
import datetime


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'remaining', 'price']

        labels = {
            'name': 'Name',
            'remaining': 'Quantity',
            'price': 'Price',
        }
    # add a custom validator

    def clean_remaining(self):
        remaining = self.cleaned_data.get('remaining')
        if remaining < 1:
            raise forms.ValidationError('Quantity cannot be negative')
        return remaining

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('Price cannot be negative')
        return price


class SalesForm(ModelForm):
    class Meta:
        model = Sales
        fields = ['item', 'quantity']

        def __str__(self):
            return f"{self.name} quantity: {self.quantity} price: {self.price} day: {self.day}"
        labels = {
            'item': 'Name',
            'quantity': 'Quantity',
        }
        constraints = {
            'quantity': {
                'min_value': 0,
            },
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError(
                "You can't sell less than 1")
        return quantity

    def clean_date(self):
        date = self.cleaned_data.get('date').today()
        if date != datetime.date.today():
            raise forms.ValidationError(
                "You can't sell in the future")
        return date

    def clean_item(self):
        item = self.cleaned_data.get('item')
        if item.remaining < 1:
            raise forms.ValidationError(
                "You can't sell less than 1")
        return item

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity') or 0
        item = cleaned_data.get('item')
        if quantity > item.remaining:
            raise forms.ValidationError(
                "You can't sell more than you have")
        return cleaned_data


class DeleteSalesForm(forms.Form):
    id = forms.ChoiceField(label='Sale', choices=[
        (i.id, i) for i in Sales.objects.all()])

    def clean_id(self):
        id = int(self.cleaned_data.get('id'))
        if id < 1:
            raise forms.ValidationError('ID cannot be negative')
        # check if id in database
        if id not in Sales.objects.all().values_list('id', flat=True):
            raise forms.ValidationError('ID not in database')
        return id


class DeleteInventoryForm(forms.Form):
    id = forms.ChoiceField(label='Item', choices=[
                           (i.id, i) for i in Inventory.objects.all()])

    def clean_id(self):
        id = int(self.cleaned_data.get('id'))
        if id < 1:
            raise forms.ValidationError('ID cannot be negative')
        # check if id in database
        if id not in Inventory.objects.all().values_list('id', flat=True):
            raise forms.ValidationError('ID not in database')
        return id


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
