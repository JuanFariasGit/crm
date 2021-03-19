from django import forms
from django.forms.widgets import NumberInput
from product.models import Product
from store.models import Store
from .models import StockExit
from stock_entry.models import StockEntry


class StockExitForm(forms.ModelForm):
  date_of_sale = forms.DateField(label='Data da Venda', widget=NumberInput(attrs={'type': 'date'}))
  product = forms.ModelChoiceField(Product.objects.all(), label='Produto')
  store = forms.ModelChoiceField(Store.objects.all(), label='Loja')
  quantity = forms.IntegerField(label='Quantidade')
  price_unit = forms.DecimalField(decimal_places=2, max_digits=8, label='Preço Unitário (R$)')


  class Meta:
    model = StockExit
    fields = [
      'date_of_sale',
      'product',
      'store',
      'quantity',
      'price_unit'
    ]


  def clean_quantity(self):
    qt = self.cleaned_data.get('quantity')
    p = self.cleaned_data.get('product')

    qt_p_in_stock = int(StockEntry.get_number_of_product_entries(p.id) - StockExit.get_number_of_product_exit(p.id))

    if self.instance.id:
      exit = StockExit.objects.filter(id=self.instance.id).first()
      qt_p_in_stock = exit.quantity + qt_p_in_stock

    if qt_p_in_stock < qt:
      raise forms.ValidationError(f'Disponível em estoque {qt_p_in_stock} {p.item}.')
    elif qt <= 0:
      raise forms.ValidationError(f'Apenas valores inteiros maiores que 0.')
    return qt