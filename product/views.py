from django.shortcuts import get_object_or_404
from .models import Product
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from .forms import ProductForm
from django.urls import reverse
from django.contrib import messages


class ProductListView(ListView):
  def post(self, request):
    products = Product.objects.all()
    response = {'data':
      [
        {
          "DT_RowId":f"row_{product.id}",
          "Item":product.get_link_update(),
          "Código do Produto":product.code,
          "Unidade de Medida":product.unit_of_measure,
          "Estoque Mínimo":product.level_minimum,
          "Estoque Máximo":product.level_maximum,
          "":product.get_button_delete()
        }
        
        for product in products
      ]
    }
    return JsonResponse(response)


class ProductCreateView(CreateView):
  template_name = 'product/form.html'
  form_class = ProductForm


  def form_valid(self, form):
    return super().form_valid(form)


  def get_success_url(self):
    messages.add_message(self.request, messages.SUCCESS, "Produto cadastrado com sucesso !")
    return reverse('product:main')


class ProductUpdateView(UpdateView):
  template_name = 'product/form.html'
  form_class = ProductForm


  def get_object(self):
    id = self.kwargs.get('id')
    return get_object_or_404(Product, id=id)


  def form_valid(self, form):
    return super().form_valid(form)


  def get_success_url(self):
    messages.add_message(self.request, messages.SUCCESS, "Produto atualizado com sucesso !")
    return reverse('product:main')


class ProductDeleteView(DeleteView):
  def post(self, request):
    id = request.POST.get('id')
    product = Product.objects.get(id=id)
    product.delete()
    response = {'message':'Produto deletado com sucesso !'}
    return JsonResponse(response)