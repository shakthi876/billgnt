# Generated by Django 4.0 on 2022-01-13 12:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminw', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='Product_Id',
            field=models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')]),
        ),
    ]
