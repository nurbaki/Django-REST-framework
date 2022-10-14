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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name= models.CharField(max_length=150)
    stock_amount = models.IntegerField()

    def __str__(self):
        return f"{self.name}"

class Stock(models.Model):
    Status =(
        ("1", "IN"),
        ("2", "OUT"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction = models.CharField(max_length=20, choices=Status)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.transaction

