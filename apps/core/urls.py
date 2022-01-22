from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


dashboard = login_required(views.dashboard)
inventory = login_required(views.inventory)
inventory_data = login_required(views.inventory_data)

urlpatterns = [
    path('', dashboard, name='index'),
    path('inventory/', inventory, name='inventory'),
    path('inventory/data/', inventory_data, name='inventory_data')
]
