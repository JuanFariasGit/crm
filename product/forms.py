from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    item = forms.CharField(label='Item', error_messages={'required': 'Campo obrigatório'})
    code = forms.CharField(label='Código do Produto', error_messages={'required': 'Campo obrigatório'})
    unit_of_measure = forms.CharField(label='Unidade de Medida', error_messages={'required': 'Campo obrigatório'})
    level_minimum = forms.IntegerField(label='Estoque Mínimo', error_messages={'required': 'Campo obrigatório'})
    level_maximum = forms.IntegerField(label='Estoque Máximo', error_messages={'required': 'Campo obrigatório'})

    class Meta:
        model = Product
        fields = [
          'item',
          'code',
          'unit_of_measure',
          'level_minimum',
          'level_maximum'
        ]
