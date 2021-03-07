from django.urls import path
from django.views.generic import TemplateView
from .views import ProductListView, ProductCreateView, ProductUpdateView


app_name = 'product'

urlpatterns = [
  path('', TemplateView.as_view(template_name='product/index.html'), name='index'),
  path('list/', ProductListView.as_view(), name='list'),
  path('create/', ProductCreateView.as_view(), name='create'),
  path('update/<int:id>/', ProductUpdateView.as_view(), name='update')
]