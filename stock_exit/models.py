from django.db import models
from product.models import Product
from store.models import Store
import math


class StockExit(models.Model):
  date_of_sale = models.DateField()
  product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
  store = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL)
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


  def get_date_of_sale(self):
    return self.date_of_sale.strftime('%d/%m/%Y')


  def get_link_update(self):
    return f'<a href="update/{self.id}/">{self.get_date_of_sale()}</a>'


  def get_price_unit(self):
    return f'R$ {str(self.price_unit).replace(".",",")}'


  def get_number_of_product_exit(id):
    return int(math.fsum([product_in_exit.quantity for product_in_exit in StockExit.objects.filter(product__id=id)]))


  def get_total_sale(self):
    return f'R$ {str(self.price_unit*self.quantity).replace(".",",")}'


  def get_total_revenue_by_id(id):
    return math.fsum([exit.price_unit*exit.quantity for exit in StockExit.objects.filter(product_id=id)])


  def get_button_delete(self):
    return f'<button class="btn btn-danger" onclick="deleteStockExitModal(\'{self.id}\', \'{self.get_date_of_sale()}\', \'{self.product.item}\')"><i class="far fa-trash-alt fa-lg"></i></button>'