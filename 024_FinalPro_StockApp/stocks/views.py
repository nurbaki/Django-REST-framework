from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from .models import (
    Firm,
    Stock,
    Category,
    Brand,
    Product,
)
from .serializers import (
    FirmSerializer,
    StockSerializer,
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
)


# Stock/:
class StockView(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [DjangoModelPermissions]
    # permission_classes = [IsStaffPermission] # Only StaffUser

class FirmView(viewsets.ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    permission_classes = [DjangoModelPermissions]

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [DjangoModelPermissions]

class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [DjangoModelPermissions]

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [DjangoModelPermissions]
