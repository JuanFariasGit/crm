# Generated by Django 3.1.7 on 2021-03-10 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0004_auto_20210309_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='phone',
            field=models.CharField(max_length=16),
        ),
    ]
