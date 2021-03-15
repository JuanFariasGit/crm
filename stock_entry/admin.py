from django.contrib import admin
from .models import StockEntry


class StockEntryAdmin(admin.ModelAdmin):
  list_display = ['product', 'created', 'modified']


admin.site.register(StockEntry, StockEntryAdmin)