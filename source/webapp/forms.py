from django import forms
from .models import CATEGORY_CHOICES, Product, Basket, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ 'name', 'description', 'category', 'amount', 'price']
        widgets = {'description': forms.Textarea}


class BasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = ['count']



class OrderForms(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['products']




class ProductCategory(forms.Form):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label='статус')


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")