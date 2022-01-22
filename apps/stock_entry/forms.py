from django import forms
from .models import StockEntry
from apps.product.models import Product
from apps.provider.models import Provider
from django.forms.widgets import NumberInput


class StockEntryForm(forms.ModelForm):
    purchase_date = forms.DateField(
        label='Data da Compra',
        widget=NumberInput(attrs={'type': 'date'}),
    )
    expiration_date = forms.DateField(
        label='Data de Validade',
        required=False,
        widget=NumberInput(attrs={'type': 'date'}),
    )
    product = forms.ModelChoiceField(label='Produto', queryset=None)
    provider = forms.ModelChoiceField(label='Fornecedor', queryset=None)
    quantity = forms.IntegerField(label='Quantidade')
    cost_unit = forms.DecimalField(
        label='Custo Unitário (R$)',
        decimal_places=2,
        max_digits=8,
    )

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

    def __init__(self, *args, **kwargs):
        super(StockEntryForm, self).__init__(*args, **kwargs)
        user = kwargs['initial']['user']
        self.fields['product'].queryset = Product.objects.filter(user=user)
        self.fields['provider'].queryset = Provider.objects.filter(user=user)
