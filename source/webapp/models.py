from django.core.validators import MinValueValidator
from django.db import models


DEFAULT_CATEGORY = 'other'
CATEGORY_CHOICES = (
    (DEFAULT_CATEGORY, 'Разное'),
    ('food', 'Продукты питания'),
    ('household', 'Хоз. товары'),
    ('toys', 'Детские игрушки'),
    ('appliances', 'Бытовая Техника')
)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    category = models.CharField(max_length=20, verbose_name='Категория',
                                choices=CATEGORY_CHOICES, default=DEFAULT_CATEGORY)
    amount = models.IntegerField(verbose_name='Остаток', validators=[MinValueValidator(0)])
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.name} - {self.amount}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Basket(models.Model):
    product = models.ForeignKey('webapp.Product', related_name='product', on_delete=models.PROTECT
                               ,verbose_name='продукт')
    count = models.IntegerField(verbose_name='количество', default=1)


class Order(models.Model):
    products = models.ManyToManyField('webapp.Product', related_name='продукты')
    name = models.CharField(null=False, max_length=50, verbose_name="имя")
    phone = models.CharField(null=False, max_length=10, verbose_name="телефон")
    adres = models.CharField(null=False,max_length=100, verbose_name='адрес')
    data = models.DateTimeField(auto_now=True, verbose_name='Время создания')