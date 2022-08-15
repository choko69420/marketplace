from django.db import models

# Create your models here.


class Inventory(models.Model):
    name = models.CharField(max_length=100)
    remaining = models.IntegerField()
    sold = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} remaining: {self.remaining} sold: {self.sold} price(for 1): {self.price}"


class Sales(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    day = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} quantity: {self.quantity} price: {self.price} day: {self.day}"
