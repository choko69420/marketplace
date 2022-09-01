from unicodedata import name
from django.db import models

# Create your models here.


class Inventory(models.Model):
    name = models.CharField(max_length=100)
    remaining = models.IntegerField()
    sold = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name}"


class Sales(models.Model):
    item = models.ForeignKey(
        Inventory, related_name='sales', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    day = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"id: {self.id}, {self.item.name} quantity: {self.quantity} price: {self.item.price} day: {self.day}"
