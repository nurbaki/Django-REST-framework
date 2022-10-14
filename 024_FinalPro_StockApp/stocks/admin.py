from django.contrib import admin

from .models import (
    Firm,
    Stock,
    Category,
    Brand,
    Product,
)
admin.site.register(Firm)
admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)

