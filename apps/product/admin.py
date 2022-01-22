from django.contrib import admin
from .models import Product
from .forms import ProductForm


class ProductAdmin(admin.ModelAdmin):
    list_display = ['item', 'created', 'modified']


admin.site.register(Product, ProductAdmin)
