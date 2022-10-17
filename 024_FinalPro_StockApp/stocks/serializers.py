from rest_framework import serializers
from .models import (
    Firm,
    Stock,
    Category,
    Brand,
    Product,
)

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        # fields = '__all__'
        exclude = (
            "price_total",
            "user",
        )

class FirmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Firm
        fields = '__all__'