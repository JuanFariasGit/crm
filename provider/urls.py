from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import (
                    ProviderListView,
                    ProviderCreateView,
                    ProviderUpdateView,
                    ProviderDeleteView
                    )


app_name = 'provider'

main = login_required(TemplateView.as_view(template_name='provider/main.html'))
list = login_required(ProviderListView.as_view())
create = login_required(ProviderCreateView.as_view())
update = login_required(ProviderUpdateView.as_view())
delete = login_required(ProviderDeleteView.as_view())

urlpatterns = [
    path('', main, name='main'),
    path('list/', list, name='list'),
    path('create/', create, name='create'),
    path('update/<int:id>/', update, name='update'),
    path('delete/', delete, name='delete')
]
