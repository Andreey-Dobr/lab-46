# Generated by Django 3.1.2 on 2020-10-22 11:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='count',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='количество'),
        ),
    ]