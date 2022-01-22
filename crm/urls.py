from decouple import config
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_required
from apps.core import views
from crm import settings

dashboard = login_required(views.dashboard)
inventory = login_required(views.inventory)
inventory_data = login_required(views.inventory_data)

urlpatterns = [
    path('', include('apps.core.urls')),
    path('account/', include('apps.profile.urls')),
    path('product/', include('apps.product.urls')),
    path('provider/', include('apps.provider.urls')),
    path('store/', include('apps.store.urls')),
    path('stock_entry/', include('apps.stock_entry.urls')),
    path('stock_exit/', include('apps.stock_exit.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
