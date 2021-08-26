from django import forms
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.forms.widgets import NumberInput
from product.models import Product
from stock_entry.models import StockEntry
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


    def clean_quantity(self):
        qt = self.cleaned_data.get('quantity')
        p = self.cleaned_data.get('product')

        total_product_entry_of_stock = StockEntry.objects.filter(product__item=p.item, user=p.user). \
            aggregate(qt=Coalesce(Sum('quantity'), 0))
        total_product_exit_of_stock = StockExit.objects.filter(product__item=p.item, user=p.user). \
            aggregate(qt=Coalesce(Sum('quantity'), 0))
        total_product_in_stock = total_product_entry_of_stock['qt'] - total_product_exit_of_stock['qt']

        if self.instance.id:
            exit = StockExit.objects.filter(id=self.instance.id, user=self.instance.user).first()
            qt_p_in_stock = exit.quantity + total_product_in_stock

        if qt_p_in_stock < qt:
            message = f'Disponível em estoque {qt_p_in_stock} {p.item}.'
            raise forms.ValidationError(message)
        elif qt <= 0:
            message = 'Apenas valores inteiros maiores que 0.'
            raise forms.ValidationError(message)
