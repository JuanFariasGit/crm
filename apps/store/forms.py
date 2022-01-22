from django import forms
from .models import Store


class StoreForm(forms.ModelForm):
    store = forms.CharField(label='Loja')
    phone = forms.CharField(label='Telefone')
    email = forms.EmailField(label='E-mail')
    address = forms.CharField(label='Endereço')

    class Meta:
        model = Store
        fields = [
          'store',
          'phone',
          'email',
          'address'
        ]
