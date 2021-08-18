from django.shortcuts import get_object_or_404
from .models import Product
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from .forms import ProductForm
from django.contrib import messages


class ProductListView(ListView):
    @staticmethod
    def post(request):
        products = Product.objects.filter(user=request.user).all()
        data = {'data': [
            {
              "DT_RowId": f"row_{product.id}",
              "Item": product.get_link_update(),
              "Código do Produto": product.code,
              "Unidade de Medida": product.unit_of_measure,
              "Estoque Mínimo": product.level_minimum,
              "Estoque Máximo": product.level_maximum,
              "": product.get_button_delete()
            }

            for product in products
            ]
        }
        return JsonResponse(data=data, status=200)


class ProductCreateView(CreateView):
    template_name = 'product/form.html'
    form_class = ProductForm
    success_message = 'Produto cadastrado com sucesso !'
    error_message = 'Erro ao cadastrar produto !'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    template_name = 'product/form.html'
    form_class = ProductForm
    success_message = 'Produto atualizado com sucesso !'
    error_message = 'Erro ao atualizar produto !'

    def get_object(self, **kwargs):
        product_id = self.kwargs.get('id')
        return get_object_or_404(Product, id=product_id, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class ProductDeleteView(DeleteView):
    @staticmethod
    def post(request, **kwargs):
        product_id = request.POST.get('id')
        product = Product.objects.filter(id=product_id, user=request.user).first()
        if product:
            product.delete()
            data = {'type': 'success', 'message': 'Produto deletado com sucesso !'}
            status = 200
        else:
            data = {'type': 'danger', 'message': 'Produto inexistente !'}
            status = 404
        return JsonResponse(data=data, status=status)
