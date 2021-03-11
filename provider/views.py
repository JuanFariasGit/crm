from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Provider
from django.http import JsonResponse
from .forms import ProviderForm
from django.contrib import messages
from django.urls import reverse


class ProviderListView(ListView):
  def post(self, request):
    providers = Provider.objects.all()
    response = {'data':
      [
        {
          "DT_RowId":f"row_{provider.id}",
          "Empresa":provider.get_link_update(),
          "Telefone":provider.phone,
          "E-mail":provider.email,
          "Endereço":provider.address,
          "":provider.get_button_delete()
        }
        
        for provider in providers
      ]
    }
    return JsonResponse(response)


class ProviderCreateView(CreateView):
  template_name = 'provider/form.html'
  form_class = ProviderForm


  def form_valid(self, form):
    return super().form_valid(form)


  def get_success_url(self):
    messages.add_message(self.request, messages.SUCCESS, "Fornecedor cadastrado com sucesso !")
    return reverse('provider:main')


class ProviderUpdateView(UpdateView):
  template_name = 'provider/form.html'
  form_class = ProviderForm


  def get_object(self):
    id = self.kwargs.get('id')
    return get_object_or_404(Provider, id=id)


  def form_valid(self, form):
    return super().form_valid(form)


  def get_success_url(self):
    messages.add_message(self.request, messages.SUCCESS, "Fornecedor atualizado com sucesso !")
    return reverse('provider:main')


class ProviderDeleteView(DeleteView):
  def post(self, request):
    id = request.POST.get('id')
    provider = Provider.objects.get(id=id)
    provider.delete()
    response = {'message':'Empresa deletada com sucesso !'}
    return JsonResponse(response)