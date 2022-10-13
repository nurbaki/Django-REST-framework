from django.db import models
from django.contrib.auth.models import User

class Firm(models.Model):
    name= models.CharField(max_length=60)
    phone = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Category(models.Model):
    name= models.CharField(max_length=60)

    def __str__(self):
        return f"{self.name}"


class Brand(models.Model):
    name= models.CharField(max_length=60)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    category = models.ForeignKey(Firm, on_delete=models.CASCADE)
    brand = models.ForeignKey(Firm, on_delete=models.CASCADE)
    name= models.CharField(max_length=150)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.name}"

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.DecimalField()
    price_total = models.DecimalField()

    def __str__(self):
        return self.transaction

