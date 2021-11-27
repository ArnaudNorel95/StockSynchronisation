from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class User(AbstractUser):
    full_name = models.CharField(max_length=50, null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.full_name

class Product(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    gtin = models.BigIntegerField(default=0)
    price = models.FloatField(default=0)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.full_name

class Synchronisation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_sent = models.DateTimeField(null=True, blank=True)
    date_effective = models.DateTimeField(null=True, blank=True)

    def __get_date_sent__(self):
        return self.date_sent

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    shortest_expiry_date = models.DateTimeField(null=True, blank=True)
    shortest_headcount = models.IntegerField(default=0)
    total_headcount = models.IntegerField(default=0)
    last_synchronisation = models.ForeignKey(Synchronisation, on_delete=models.CASCADE, null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default=1)
