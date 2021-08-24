from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Store(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.CharField(max_length=100)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'store'
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

    def __str__(self):
        return self.store

    @staticmethod
    def get_absolute_url():
        return reverse('store:main')

    def get_link_update(self):
        return f'<a href="update/{self.id}/">{self.store}</a>'

    def get_button_delete(self):
        return f"<button class=\"btn btn-danger\" onclick=\"deleteStoreModal(\'{self.id}\',\'{self.store}\')\">" \
               "<i class=\"far fa-trash-alt fa-lg\"></i></button>"
