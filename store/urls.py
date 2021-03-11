from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import StoreListView, StoreCreateView, StoreUpdateView, StoreDeleteView


app_name = 'store'

urlpatterns = [
  path('', login_required(TemplateView.as_view(template_name='store/main.html')), name='main'),
  path('list/', login_required(StoreListView.as_view()), name='list'),
  path('create/', login_required(StoreCreateView.as_view()), name='create'),
  path('update/<int:id>/', login_required(StoreUpdateView.as_view()), name='update'),
  path('delete/', login_required(StoreDeleteView.as_view()), name='delete')
]