from django.shortcuts import get_object_or_404
from .forms import StockExitForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import StockExit
from django.http import JsonResponse
from django.contrib import messages


class StockExitListView(ListView):
  def post(self, request):
    stock_exit = StockExit.objects.all()
    response = {"data":
      [
        {
          "DT_RowId":f"row_{exit.id}",
          "Data da Venda":exit.get_link_update(),
          "Produto":exit.product.item if exit.product else '',
          "Loja":exit.store.store,
          "Quantidade":exit.quantity,
          "Preço Unitário":exit.get_price_unit(),
          "Total":exit.get_total_sale(),
          "":exit.get_button_delete()
        }

        for exit in stock_exit
      ]
    }
    return JsonResponse(response)


class StockExitCreateView(CreateView):
  template_name = 'stock_exit/form.html'
  form_class = StockExitForm


  def form_valid(self, form):
    return super().form_valid(form)


  def get_success_url(self):
    messages.add_message(self.request, messages.SUCCESS, "Saída cadastrada com sucesso !")
    return reverse('stock_exit:main')


class StockExitUpdateView(UpdateView):
  template_name = 'stock_exit/form.html'
  form_class = StockExitForm


  def get_object(self):
    id = self.kwargs.get('id')
    return get_object_or_404(StockExit, id=id)


  def form_valid(self, form):
    return super().form_valid(form)


  def get_success_url(self):
    messages.add_message(self.request, messages.SUCCESS, "Saída atualizada com sucesso !")
    return reverse('stock_exit:main')


class StockExitDeleteView(DeleteView):
  def post(self, request):
    id = request.POST.get('id')
    exit = StockExit.objects.get(id=id)
    exit.delete()
    response = {'message': 'Saída deletada com sucesso !'}
    return JsonResponse(response)