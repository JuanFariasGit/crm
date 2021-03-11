from django import forms
from .models import StockEntry
from product.models import Product
from provider.models import Provider


class DateInput(forms.DateInput):
    input_type = "date"


class StockEntryForm(forms.ModelForm):
  purchase_date = forms.DateField(label='Data da Compra', widget=DateInput())
  product = forms.ModelChoiceField(Product.objects.all(), label='Produto')
  provider = forms.ModelChoiceField(Provider.objects.all(), label='Fornecedor')
  quantity = forms.IntegerField(label='Quantidade')


  class Meta:
    model = StockEntry
    fields = [
      'purchase_date',
      'product',
      'provider',
      'quantity'
    ]