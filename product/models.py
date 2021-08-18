from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    code = models.CharField(max_length=13)
    unit_of_measure = models.CharField(max_length=30)
    level_minimum = models.IntegerField()
    level_maximum = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.item

    @staticmethod
    def get_absolute_url():
        return reverse('product:main')

    def get_link_update(self):
        return f'<a href="update/{self.id}/">{self.item}</a>'

    def get_button_delete(self):
        return f"""
        <button
        class="btn btn-danger"
        onclick="deleteProductModal(
        \'{self.id}\',
        \'{self.item}\')">
        <i class="far fa-trash-alt fa-lg">
        </i></button>
        """
