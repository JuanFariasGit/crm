from django import forms
from .models import StockEntry
from product.models import Product
from provider.models import Provider
from django.forms.widgets import NumberInput


class StockEntryForm(forms.ModelForm):
  purchase_date = forms.DateField(label='Data da Compra', widget=NumberInput(attrs={'type': 'date'}))
  expiration_date = forms.DateField(label='Data de Validade', widget=NumberInput(attrs={'type': 'date'}))
  product = forms.ModelChoiceField(Product.objects.all(), label='Produto')
  provider = forms.ModelChoiceField(Provider.objects.all(), label='Fornecedor')
  quantity = forms.IntegerField(label='Quantidade')
  cost_unit = forms.DecimalField(label='Custo Unitário (R$)', decimal_places=2, max_digits=8)


  class Meta:
    model = StockEntry
    fields = [
      'purchase_date',
      'expiration_date',
      'product',
      'provider',
      'quantity',
      'cost_unit'
    ]