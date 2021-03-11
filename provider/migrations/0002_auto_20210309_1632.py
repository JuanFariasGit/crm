# Generated by Django 3.1.7 on 2021-03-09 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='provider',
            options={'verbose_name': 'Provider', 'verbose_name_plural': 'Providers'},
        ),
        migrations.AddField(
            model_name='provider',
            name='area_code',
            field=models.CharField(default=-1.0, max_length=3),
            preserve_default=False,
        ),
    ]