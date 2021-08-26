from django import forms
from django.forms.widgets import NumberInput
from product.models import Product
from store.models import Store
from .models import StockExit


class StockExitForm(forms.ModelForm):
    date_of_sale = forms.DateField(
        label='Data da Venda',
        widget=NumberInput(attrs={'type': 'date'}),
    )
    product = forms.ModelChoiceField(label='Produto', queryset=None)
    store = forms.ModelChoiceField(label='Loja', queryset=None)
    quantity = forms.IntegerField(label='Quantidade')
    price_unit = forms.DecimalField(
        decimal_places=2,
        max_digits=8,
        label='Preço Unitário (R$)',
    )

    class Meta:
        model = StockExit
        fields = [
          'date_of_sale',
          'product',
          'store',
          'quantity',
          'price_unit'
        ]

    def __init__(self, *args, **kwargs):
        super(StockExitForm, self).__init__(*args, **kwargs)
        user = kwargs['initial']['user']
        self.fields['product'].queryset = Product.objects.filter(user=user)
        self.fields['store'].queryset = Store.objects.filter(user=user)
