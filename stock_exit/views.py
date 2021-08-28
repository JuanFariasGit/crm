from django.shortcuts import get_object_or_404
from .forms import StockExitForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import StockExit
from django.http import JsonResponse
from django.contrib import messages


class StockExitListView(ListView):
    @staticmethod
    def post(request):
        stock_exit = StockExit.objects.filter(user=request.user)
        data = {"data": [
            {
              "DT_RowId": f"row_{exit_.id}",
              "Data da Venda": exit_.get_link_update(),
              "Produto": exit_.product.item,
              "Loja": exit_.store.store,
              "Quantidade": exit_.quantity,
              "Preço Unitário": exit_.get_price_unit(),
              "Total": exit_.get_total_sale(),
              "": exit_.get_button_delete()
            }

            for exit_ in stock_exit
            ]
        }
        return JsonResponse(data=data, status=200)


class StockExitCreateView(CreateView):
    template_name = 'stock_exit/form.html'
    form_class = StockExitForm
    success_message = 'Saída cadastrada com sucesso !'
    error_message = 'Erro ao cadastrar saída !'

    def get_initial(self, *args, **kwargs):
        initial = super(StockExitCreateView, self).get_initial(**kwargs)
        initial['user'] = self.request.user
        return initial

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
    success_message = 'Saída atualizada com sucesso !'
    error_message = 'Erro ao atualizar saída !'

    def get_initial(self, *args, **kwargs):
        initial = super(StockExitUpdateView, self).get_initial(**kwargs)
        initial['user'] = self.request.user
        return initial

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
            status = 200
        else:
            data = {'type': 'danger', 'message': 'Saída inexistente !'}
            status = 404
        return JsonResponse(data=data, status=status)
