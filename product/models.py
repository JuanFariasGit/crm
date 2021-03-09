from django.db import models


class Product(models.Model):
  item = models.CharField(max_length=100)
  code = models.CharField(max_length=13)
  unit_of_measure = models.CharField(max_length=30)
  level_minimum = models.IntegerField()
  cost_unit = models.DecimalField(decimal_places=2, max_digits=8)
  price_unit = models.DecimalField(decimal_places=2, max_digits=8)
  
  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'product'
    verbose_name = 'Product'
    verbose_name_plural = 'Products'


  def __str__(self):
    return self.item


  def get_link_update(self):
    return f'<a href="update/{self.id}/">{self.item}</a>'


  def get_button_delete(self):
    return f'<button class="btn btn-danger" onclick="deleteProductModal(\'{self.id}\', \'{self.item}\')"><i class="far fa-trash-alt fa-lg"></button>'


  def get_cost_unit(self):
    return f'R$ {str(self.cost_unit).replace(".",",")}'


  def get_price_unit(self):
    return  f'R$ {str(self.price_unit).replace(".",",")}'