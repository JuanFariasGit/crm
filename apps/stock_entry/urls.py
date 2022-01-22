from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import (
                    StockEntryListView,
                    StockEntryCreateView,
                    StockEntryUpdateView,
                    StockEntryDeleteView
                    )


app_name = 'stock_entry'

main = login_required(
    TemplateView.as_view(template_name='stock_entry/main.html'),
)
list = login_required(StockEntryListView.as_view())
create = login_required(StockEntryCreateView.as_view())
update = login_required(StockEntryUpdateView.as_view())
delete = login_required(StockEntryDeleteView.as_view())

urlpatterns = [
    path('', main, name='main'),
    path('list/', list, name='list'),
    path('create/', create, name='create'),
    path('update/<int:id>/', update, name='update'),
    path('delete/', delete, name='delete')
]
