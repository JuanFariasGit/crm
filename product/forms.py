from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
  code = forms.CharField(label='Código do Produto')
  item = forms.CharField(label='Item')
  unit_of_measure = forms.CharField(label='Unidade de Medida')
  level_minimum = forms.IntegerField(label='Estoque Mínimo')
  cost_unit = forms.DecimalField(label='Custo Unitario (R$)')
  price_unit = forms.DecimalField(label='Preço Unitario (R$)')


  class Meta:
    model = Product
    fields = [
      'code',
      'item',
      'unit_of_measure',
      'level_minimum',
      'cost_unit',
      'price_unit'
    ]