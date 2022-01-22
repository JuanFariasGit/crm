from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import (StoreListView,
                    StoreCreateView,
                    StoreUpdateView,
                    StoreDeleteView
                    )


app_name = 'store'

main = login_required(TemplateView.as_view(template_name='store/main.html'))
list = login_required(StoreListView.as_view())
create = login_required(StoreCreateView.as_view())
update = login_required(StoreUpdateView.as_view())
delete = login_required(StoreDeleteView.as_view())

urlpatterns = [
    path('', main, name='main'),
    path('list/', list, name='list'),
    path('create/', create, name='create'),
    path('update/<int:id>/', update, name='update'),
    path('delete/', delete, name='delete')
]
