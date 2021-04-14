from django import forms
from .models import Provider


class ProviderForm(forms.ModelForm):
    company = forms.CharField(label='Empresa')
    phone = forms.CharField(label='Telefone')
    email = forms.EmailField(label='E-mail')
    address = forms.CharField(label='Endereço')

    class Meta:
        model = Provider
        fields = [
          'company',
          'phone',
          'email',
          'address'
        ]
