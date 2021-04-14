from django.db import models


class Provider(models.Model):
    company = models.CharField(max_length=100)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    address = models.CharField(max_length=250)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'provider'
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'

    def __str__(self):
        return self.company

    def get_link_update(self):
        return f'<a href="update/{self.id}/">{self.company}</a>'

    def get_button_delete(self):
        return f"""
        <button
        class="btn btn-danger"
        onclick="deleteProviderModal(
        \'{self.id}\',
        \'{self.company}\')">
        <i class="far fa-trash-alt fa-lg"></i>
        </button>"""
