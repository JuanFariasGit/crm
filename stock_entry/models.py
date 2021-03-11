from django.db import models
from product.models import Product
from provider.models import Provider


class StockEntry(models.Model):
  purchase_date = models.DateField()
  product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
  provider = models.ForeignKey(Provider, null=True, on_delete=models.SET_NULL)
  quantity = models.IntegerField()

  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)


  class Meta:
    db_table = 'stock_entry'
    verbose_name = 'Stock Entry'
    verbose_name_plural = 'Stock Entry'


  def __str__(self):
    return product.item


  def get_purchase_date(self):
        return self.purchase_date.strftime('%d/%m/%Y')


  def get_total_purchase(self):
    return f'R$ {str(self.product.cost_unit*self.quantity).replace(".",",")}'


  def get_link_update(self):
    return f'<a href="update/{self.id}/">{self.get_purchase_date()}</a>'


  def get_button_delete(self):
    return f'<button class="btn btn-danger" onclick="deleteStockEntryModal(\'{self.id}\', \'{self.get_purchase_date()}\', \'{self.product.item}\')"><i class="far fa-trash-alt fa-lg"></i></button>'