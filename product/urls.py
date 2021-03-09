from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView


app_name = 'product'

urlpatterns = [
  path('', login_required(TemplateView.as_view(template_name='product/index.html')), name='index'),
  path('list/', login_required(ProductListView.as_view()), name='list'),
  path('create/', login_required(ProductCreateView.as_view()), name='create'),
  path('update/<int:id>/', login_required(ProductUpdateView.as_view()), name='update'),
  path('delete/', login_required(ProductDeleteView.as_view()), name='delete')
]