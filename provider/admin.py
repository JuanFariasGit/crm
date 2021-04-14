from django.contrib import admin
from .models import Provider


class ProviderAdmin(admin.ModelAdmin):
    list_display = ['company', 'created', 'modified']


admin.site.register(Provider, ProviderAdmin)
