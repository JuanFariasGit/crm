from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Provider
from django.http import JsonResponse
from .forms import ProviderForm
from django.contrib import messages


class ProviderListView(ListView):
    @staticmethod
    def post(request):
        providers = Provider.objects.filter(user=request.user).all()
        data = {'data': [
            {
              "DT_RowId": f"row_{provider.id}",
              "Empresa": provider.get_link_update(),
              "Telefone": provider.phone,
              "E-mail": provider.email,
              "Endereço": provider.address,
              "": provider.get_button_delete()
            }

            for provider in providers
            ]
        }
        return JsonResponse(data=data, status=200)


class ProviderCreateView(CreateView):
    template_name = 'provider/form.html'
    form_class = ProviderForm
    success_message = 'Fornecedor cadastrado com sucesso !'
    error_message = 'Erro ao cadastrar fornecedor !'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class ProviderUpdateView(UpdateView):
    template_name = 'provider/form.html'
    form_class = ProviderForm
    success_message = 'Fornecedor atualizado com sucesso !'
    error_message = 'Erro ao atualizar fornecedor !'

    def get_object(self, **kwargs):
        provider_id = self.kwargs.get('id')
        return get_object_or_404(Provider, id=provider_id, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class ProviderDeleteView(DeleteView):
    @staticmethod
    def post(request, **kwargs):
        provider_id = request.POST.get('id')
        provider = Provider.objects.filter(id=provider_id, user=request.user).first()
        if provider:
            provider.delete()
            data = {'type': 'success', 'message': 'Fornecedor deletado com sucesso !'}
            status = 200
        else:
            data = {'type': 'danger', 'message': 'Fornecedor inexistente !'}
            status = 404
        return JsonResponse(data=data, status=status)
