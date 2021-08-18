from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from product.models import Product
from store.models import Store
from ultils.ultils import currency_format, date_format


class StockExit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_sale = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_unit = models.DecimalField(decimal_places=2, max_digits=8)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stock_exit'
        verbose_name = 'Stock Exit'
        verbose_name_plural = 'Stock Exit'

    def __str__(self):
        return self.product.item

    def get_absolute_url(self):
        return reverse('stock_exit:main')

    def get_date_of_sale(self):
        return date_format(self.date_of_sale)

    def get_link_update(self):
        return f'<a href="update/{self.id}/">{self.get_date_of_sale()}</a>'

    def get_price_unit(self):
        return currency_format(self.price_unit)

    def get_total_sale(self):
        return currency_format(self.price_unit*self.quantity)

    def get_button_delete(self):
        return f"""
        <button class="btn btn-danger"
        onclick="deleteStockExitModal(
        \'{self.id}\',
        \'{self.get_date_of_sale()}\',
        \'{self.product.item}\')">
        <i class="far fa-trash-alt fa-lg"></i>
        </button>"""
