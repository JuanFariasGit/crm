from django.contrib import admin
from .models import StockExit


class StockExitAdmin(admin.ModelAdmin):
    list_display = ['product', 'created', 'modified']


admin.site.register(StockExit, StockExitAdmin)
