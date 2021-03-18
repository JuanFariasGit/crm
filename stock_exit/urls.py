from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import StockExitListView, StockExitCreateView, StockExitUpdateView, StockExitDeleteView


app_name = 'stock_exit'

urlpatterns = [
  path('', login_required(TemplateView.as_view(template_name='stock_exit/main.html')), name='main'),
  path('list/', login_required(StockExitListView.as_view()), name='list'),
  path('create/', login_required(StockExitCreateView.as_view()), name='create'),
  path('update/<int:id>/', login_required(StockExitUpdateView.as_view()), name='update'),
  path('delete/', login_required(StockExitDeleteView.as_view()), name='delete')
]
