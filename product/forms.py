from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    item = forms.CharField(label='Item')
    code = forms.CharField(label='Código do Produto')
    unit_of_measure = forms.CharField(label='Unidade de Medida')
    level_minimum = forms.IntegerField(label='Estoque Mínimo')
    level_maximum = forms.IntegerField(label='Estoque Máximo')

    class Meta:
        model = Product
        fields = [
          'item',
          'code',
          'unit_of_measure',
          'level_minimum',
          'level_maximum'
        ]