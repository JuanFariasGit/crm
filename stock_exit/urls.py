from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import (
                    StockExitListView,
                    StockExitCreateView,
                    StockExitUpdateView,
                    StockExitDeleteView
                    )


app_name = 'stock_exit'

main = login_required(
    TemplateView.as_view(template_name='stock_exit/main.html'),
)
list = login_required(StockExitListView.as_view())
create = login_required(StockExitCreateView.as_view())
update = login_required(StockExitUpdateView.as_view())
delete = login_required(StockExitDeleteView.as_view())

urlpatterns = [
    path('', main, name='main'),
    path('list/', list, name='list'),
    path('create/', create, name='create'),
    path('update/<int:id>/', update, name='update'),
    path('delete/', delete, name='delete')
]
