from django.shortcuts import get_object_or_404
from .forms import StockExitForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import StockExit
from django.http import JsonResponse
from django.contrib import messages


class StockExitListView(ListView):
    @staticmethod
    def post(request):
        stock_exit = StockExit.objects.filter(user=request.user).all()
        data = {"data": [
            {
              "DT_RowId": f"row_{exit.id}",
              "Data da Venda": exit.get_link_update(),
              "Produto": exit.product.item,
              "Loja": exit.store.store,
              "Quantidade": exit.quantity,
              "Preço Unitário": exit.get_price_unit(),
              "Total": exit.get_total_sale(),
              "": exit.get_button_delete()
            }

            for exit in stock_exit
            ]
        }
        return JsonResponse(data=data, status=200)


class StockExitCreateView(CreateView):
    template_name = 'stock_exit/form.html'
    form_class = StockExitForm
    success_message = 'Saída cadastrada com sucesso !'
    error_message = 'Erro ao cadastra saída !'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class StockExitUpdateView(UpdateView):
    template_name = 'stock_exit/form.html'
    form_class = StockExitForm
    success_message = 'Saída atualizar com sucesso !'
    error_message = 'Erro ao atualizar saída !'

    def get_object(self, **kwargs):
        exit_id = self.kwargs.get('id')
        return get_object_or_404(StockExit, id=exit_id, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class StockExitDeleteView(DeleteView):
    @staticmethod
    def post(request, **kwargs):
        exit_id = request.POST.get('id')
        exit = StockExit.objects.filter(id=exit_id, user=request.user).first()
        if exit:
            exit.delete()
            data = {'type': 'success', 'message': 'Saída deletada com sucesso !'}
        else:
            data = {'type': 'danger', 'message': 'Saída inexistente !'}
        return JsonResponse(data=data, status=200)
