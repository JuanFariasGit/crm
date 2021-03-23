from django.db import models
from product.models import Product
from provider.models import Provider
from stock_exit.models import StockExit
import math
from ultils.ultils import currency_format, date_format


class StockEntry(models.Model):
  purchase_date = models.DateField()
  expiration_date = models.DateField(null=True, blank=True)
  product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
  provider = models.ForeignKey(Provider, null=True, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  cost_unit = models.DecimalField(decimal_places=2, max_digits=8)

  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)


  class Meta:
    db_table = 'stock_entry'
    verbose_name = 'Stock Entry'
    verbose_name_plural = 'Stock Entry'


  def __str__(self):
    return self.product.item


  def get_purchase_date(self):
    return date_format(self.purchase_date)


  def get_total_purchase(self):
    return currency_format(self.cost_unit*self.quantity)


  def get_cost_unit(self):
    return currency_format(self.cost_unit)


  def get_total_cost():
    return math.fsum([entry.cost_unit*entry.quantity for entry in StockEntry.objects.all()])


  def get_total_cost_by_id(id):
    return math.fsum([entry.cost_unit*entry.quantity for entry in StockEntry.objects.filter(product__id=id)])


  def get_number_of_product_entries(id):
    return math.fsum([product_in_entry.quantity for product_in_entry in StockEntry.objects.filter(product__id=id)])


  def get_expiration_date(self):
    if self.expiration_date is None:
      return "Sem validade"
    else:
      return date_format(self.expiration_date)


  def get_link_update(self):
    return f'<a href="update/{self.id}/">{self.get_purchase_date()}</a>'


  def get_button_delete(self):
    return f'<button class="btn btn-danger" onclick="deleteStockEntryModal(\'{self.id}\', \'{self.get_purchase_date()}\', \'{self.product.item}\')"><i class="far fa-trash-alt fa-lg"></i></button>'