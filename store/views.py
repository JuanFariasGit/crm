from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Store
from django.http import JsonResponse
from .forms import StoreForm
from django.contrib import messages


class StoreListView(ListView):
    @staticmethod
    def post(request):
        stores = Store.objects.filter(user=request.user).all()
        data = {'data': [
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
        return JsonResponse(data=data, status=200)


class StoreCreateView(CreateView):
    template_name = 'store/form.html'
    form_class = StoreForm
    success_message = 'Loja cadastrada com sucesso !'
    error_message = 'Erro ao cadastrar loja !'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class StoreUpdateView(UpdateView):
    template_name = 'store/form.html'
    form_class = StoreForm
    success_message = 'Loja atualizada com sucesso !'
    error_message = 'Erro ao atualizar loja !'

    def get_object(self, **kwargs):
        store_id = self.kwargs.get('id')
        return get_object_or_404(Store, id=store_id, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class StoreDeleteView(DeleteView):
    @staticmethod
    def post(request, **kwargs):
        store_id = request.POST.get('id')
        store = Store.objects.filter(id=store_id, user=request.user).first()
        if store:
            store.delete()
            data = {'type': 'success', 'message': 'Loja deletada com sucesso !'}
            status=200
        else:
            data = {'type': 'danger', 'message': 'Loja inexistente !'}
            status=404
        return JsonResponse(data=data, status=status)
