from django.db import models


class Product(models.Model):
  item = models.CharField(max_length=100)
  code = models.CharField(max_length=13)
  unit_of_measure = models.CharField(max_length=30)
  level_minimum = models.IntegerField()
  cost_unit = models.DecimalField(decimal_places=2, max_digits=8)
  price_unit = models.DecimalField(decimal_places=2, max_digits=8)

  reated = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = 'product'
    verbose_name = 'Produtc'
    verbose_name_plural = 'Products'


  def __str__(self):
    return self.item