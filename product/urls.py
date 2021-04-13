from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import (
                    ProductListView,
                    ProductCreateView,
                    ProductUpdateView,
                    ProductDeleteView
                    )


app_name = 'product'

main = login_required(TemplateView.as_view(template_name='product/main.html'))
list = login_required(ProductListView.as_view())
create = login_required(ProductCreateView.as_view())
update = login_required(ProductUpdateView.as_view())
delete = login_required(ProductDeleteView.as_view())

urlpatterns = [
    path('', main, name='main'),
    path('list/', list, name='list'),
    path('create/', create, name='create'),
    path('update/<int:id>/', update, name='update'),
    path('delete/', delete, name='delete')
]
