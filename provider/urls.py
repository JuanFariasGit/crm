from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import ProviderListView, ProviderCreateView, ProviderUpdateView, ProviderDeleteView


app_name = 'provider'

urlpatterns = [
  path('', login_required(TemplateView.as_view(template_name='provider/main.html')), name='main'),
  path('list/', login_required(ProviderListView.as_view()), name='list'),
  path('create/', login_required(ProviderCreateView.as_view()), name='create'),
  path('update/<int:id>/', login_required(ProviderUpdateView.as_view()), name='update'),
  path('delete/', login_required(ProviderDeleteView.as_view()), name='delete')
]