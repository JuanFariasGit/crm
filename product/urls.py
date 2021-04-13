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

main = TemplateView.as_view(template_name='product/main.html')
list = ProductListView.as_view()
create = ProductCreateView.as_view()
update = ProductUpdateView.as_view()
delete = ProductDeleteView.as_view()

urlpatterns = [
    path('', login_required(main), name='main'),
    path('list/', login_required(list), name='list'),
    path('create/', login_required(create), name='create'),
    path('update/<int:id>/', login_required(update), name='update'),
    path('delete/', login_required(delete), name='delete')
]
