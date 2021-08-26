from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import StockEntry
from django.http import JsonResponse
from .forms import StockEntryForm
from django.contrib import messages


class StockEntryListView(ListView):
    @staticmethod
    def post(request):
        stock_entry = StockEntry.objects.filter(user=request.user)
        data = {"data": [
            {
              "DT_RowId": f"row_{entry.id}",
              "Data da Compra": entry.get_link_update(),
              "Produto": entry.product.item,
              "Data de Validade": entry.get_expiration_date(),
              "Fornecedor": entry.provider.company,
              "Quantidade": entry.quantity,
              "Custo Unitário": entry.get_cost_unit(),
              "Total": entry.get_total_purchase(),
              "": entry.get_button_delete()
            }

            for entry in stock_entry
            ]
        }
        return JsonResponse(data=data, status=200)


class StockEntryCreateView(CreateView):
    template_name = 'stock_entry/form.html'
    form_class = StockEntryForm
    success_message = 'Entrada cadastrada com sucesso !'
    error_message = 'Erro ao cadastrar entrada !'

    def get_initial(self, *args, **kwargs):
        initial = super(StockEntryCreateView, self).get_initial(**kwargs)
        initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, self.error_message)
        return super().form_invalid(form)


class StockEntryUpdateView(UpdateView):
    template_name = 'stock_entry/form.html'
    form_class = StockEntryForm
    success_message = 'Entrada atualizada com sucesso !'
    error_message = 'Erro ao atualizar entrada'

    def get_initial(self, *args, **kwargs):
        initial = super(StockEntryUpdateView, self).get_initial(**kwargs)
        initial['user'] = self.request.user
        return initial

    def get_object(self, **kwargs):
        entry_id = self.kwargs.get('id')
        return get_object_or_404(StockEntry, id=entry_id, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class StockEntryDeleteView(DeleteView):
    @staticmethod
    def post(request, **kwargs):
        entry_id = request.POST.get('id')
        entry = StockEntry.objects.filter(id=entry_id, user=request.user).first()
        if entry:
            entry.delete()
            data = {'type': 'success', 'message': 'Entrada deletada com sucesso !'}
            status = 200
        else:
            data = {'type': 'danger', 'message': 'Entrada inexistente !'}
            status = 404
        return JsonResponse(data=data, status=status)
