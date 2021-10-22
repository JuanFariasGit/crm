from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from product.models import Product
from provider.models import Provider

from ultils.ultils import currency_format, date_format


class StockEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost_unit = models.DecimalField(decimal_places=2, max_digits=8)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stock_entry'
        verbose_name = 'Stock Entry'
        verbose_name_plural = 'Stock Entry'

    @staticmethod
    def get_absolute_url():
        return reverse('stock_entry:main')

    def get_purchase_date(self):
        return date_format(self.purchase_date)

    def get_total_purchase(self):
        return currency_format(self.cost_unit*self.quantity)

    def get_cost_unit(self):
        return currency_format(self.cost_unit)

    def get_expiration_date(self):
        if self.expiration_date is None:
            return "Sem validade"
        else:
            return date_format(self.expiration_date)

    def get_link_update(self):
        return f'<a href="update/{self.id}/">{self.get_purchase_date()}</a>'

    def get_button_delete(self):
        return f'<button class="btn btn-danger" onclick="deleteStockEntryModal(\'{self.id}\',' \
               f'\'{self.get_purchase_date()}\',\'{self.product.item}\')">' \
               '<i class="far fa-trash-alt fa-lg"></i></button>'
