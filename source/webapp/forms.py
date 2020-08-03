from django import forms
from django.forms import widgets
from django.core.validators import MinValueValidator
from .models import CATEGORY_CHOICES, DEFAULT_CATEGORY



class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='название')
    description = forms.CharField(max_length=3000, required=True, label='Подробное описание',
                                  widget=widgets.Textarea)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, initial=DEFAULT_CATEGORY, label='статус')
    amount = forms.IntegerField(validators=[MinValueValidator(0)], label='количество')
    price = forms.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)], label='цена')


class ProductCategory(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label='статус')