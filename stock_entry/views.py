from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import StockEntry
from django.http import JsonResponse
from .forms import StockEntryForm
from django.urls import reverse
from django.contrib import messages


class StockEntryListView(ListView):
    def post(self, request):
        stock_entry = StockEntry.objects.all()
        response = {"data": [
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
        return JsonResponse(response)


class StockEntryCreateView(CreateView):
    template_name = 'stock_entry/form.html'
    form_class = StockEntryForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        message = "Entrada cadastrada com sucesso !"
        messages.add_message(self.request, messages.SUCCESS, message)
        return reverse('stock_entry:main')


class StockEntryUpdateView(UpdateView):
    template_name = 'stock_entry/form.html'
    form_class = StockEntryForm

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(StockEntry, id=id)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        message = "Entrada atualizada com sucesso !"
        messages.add_message(self.request, messages.SUCCESS, message)
        return reverse('stock_entry:main')


class StockEntryDeleteView(DeleteView):
    def post(self, request):
        id = request.POST.get('id')
        entry = StockEntry.objects.get(id=id)
        entry.delete()
        response = {'message': 'Entrada deletada com sucesso !'}
        return JsonResponse(response)
