from django.db import models
from product.models import Product
from provider.models import Provider
from stock_exit.models import StockExit
import math


class StockEntry(models.Model):
  purchase_date = models.DateField()
  expiration_date = models.DateField(null=True)
  product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
  provider = models.ForeignKey(Provider, null=True, on_delete=models.SET_NULL)
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
        return self.purchase_date.strftime('%d/%m/%Y')


  def get_total_purchase(self):
    return f'R$ {str(self.cost_unit*self.quantity).replace(".",",")}'


  def get_cost_unit(self):
    return f'R$ {str(self.cost_unit).replace(".",",")}'


  def get_total_cost():
    return str(f'R$ {math.fsum([entry.cost_unit*entry.quantity for entry in StockEntry.objects.all()]):.2f}').replace('.',',')


  def get_total_cost_by_id(id):
    return math.fsum([entry.cost_unit*entry.quantity for entry in StockEntry.objects.filter(product__id=id)])


  def get_number_of_product_entries(id):
    return int(math.fsum([product_in_entry.quantity for product_in_entry in StockEntry.objects.filter(product__id=id)]))


  def get_expiration_date(self):
    if self.expiration_date is None:
      return "Sem validade"
    else:
      return self.expiration_date.strftime('%d/%m/%Y')


  def get_link_update(self):
    return f'<a href="update/{self.id}/">{self.get_purchase_date()}</a>'


  def get_button_delete(self):
    return f'<button class="btn btn-danger" onclick="deleteStockEntryModal(\'{self.id}\', \'{self.get_purchase_date()}\', \'{self.product.item}\')"><i class="far fa-trash-alt fa-lg"></i></button>'