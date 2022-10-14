from django.contrib import admin

from seller.models import Product, Seller

# Register your models here.

admin.site.register(Seller)
admin.site.register(Product)

