from django.contrib import admin
from .models import Store


class StoreAdmin(admin.ModelAdmin):
    list_display = ['store', 'created', 'modified']


admin.site.register(Store, StoreAdmin)
