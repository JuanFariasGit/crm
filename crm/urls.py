from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_required
from core import views


dashboard = login_required(views.dashboard)
inventory = login_required(views.inventory)
inventory_data = login_required(views.get_data_inventory)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('login/verify/', views.verify_login, name='verify_login'),
    path('login/logout/', views.logout, name='logout'),
    path('', dashboard, name='index'),
    path('inventory/', inventory, name='inventory'),
    path('inventory/data/', inventory_data, name='inventory-data'),
    # includes
    path('product/', include('product.urls')),
    path('provider/', include('provider.urls')),
    path('store/', include('store.urls')),
    path('stock_entry/', include('stock_entry.urls')),
    path('stock_exit/', include('stock_exit.urls'))
]
