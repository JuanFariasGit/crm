from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Store
from django.http import JsonResponse
from .forms import StoreForm
from django.contrib import messages
from django.urls import reverse


class StoreListView(ListView):
    def post(self, request):
        stores = Store.objects.all()
        response = {'data': [
            {
              "DT_RowId": f"row_{store.id}",
              "Loja": store.get_link_update(),
              "Telefone": store.phone,
              "E-mail": store.email,
              "Endereço": store.address,
              "": store.get_button_delete()
            }

            for store in stores
            ]
        }
        return JsonResponse(response)


class StoreCreateView(CreateView):
    template_name = 'store/form.html'
    form_class = StoreForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        message = "Loja cadastrada com sucesso !"
        messages.add_message(self.request, messages.SUCCESS, message)
        return reverse('store:main')


class StoreUpdateView(UpdateView):
    template_name = 'store/form.html'
    form_class = StoreForm

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Store, id=id)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        message = "Loja atualizada com sucesso !"
        messages.add_message(self.request, messages.SUCCESS, message)
        return reverse('store:main')


class StoreDeleteView(DeleteView):
    def post(self, request):
        id = request.POST.get('id')
        store = Store.objects.get(id=id)
        store.delete()
        response = {'message': 'Loja deletada com sucesso !'}
        return JsonResponse(response)
