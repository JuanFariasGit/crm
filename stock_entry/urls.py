from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import StockEntryListView, StockEntryCreateView, StockEntryUpdateView, StockEntryDeleteView


app_name = 'stock_entry'

urlpatterns = [
  path('', login_required(TemplateView.as_view(template_name='stock_entry/main.html')), name='main'),
  path('list/', login_required(StockEntryListView.as_view()), name='list'),
  path('create/', login_required(StockEntryCreateView.as_view()), name='create'),
  path('update/<int:id>/', login_required(StockEntryUpdateView.as_view()), name='update'),
  path('delete/', login_required(StockEntryDeleteView.as_view()), name='delete')
]