from django.core.serializers import serialize
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ProductForm, ProductCategory
from webapp.models import Product


class ProductListView(ListView):
    template_name = 'product/index.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 6
    ordering = ['amount']
    search_fields = ['name__icontains']


    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)

def product_list_view(request, *args, **kwargs):
    if request.method == 'GET':
        products = Product.objects.all()
        products_data = serialize('json', products)
        response = HttpResponse(products_data)
        response['Content-Type'] = 'application/json'
        return response



class ProductView(DetailView):
    template_name = 'product/product_view.html'
    model = Product


    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def category_view(request,ct):

    data = Product.objects.all().filter(category=ct)
    category = ProductCategory()
    return render(request, 'product/index.html', context={
        'products': data,
        'category': category
    })

class ProjectCreate(CreateView):
    template_name = 'product/create.html'
    form_class = ProductForm
    model = Product

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class Product_Update_View(UpdateView):
    model = Product
    template_name = 'product/update.html'
    form_class = ProductForm
    context_object_name = 'project'

    def get_success_url(self):
        return reverse('product_view', kwargs={'pk': self.object.pk})


class Delete_Product(DeleteView):
    template_name = 'product/delete.html'
    model = Product
    context_key = 'product'

    def get_success_url(self):
        return reverse('index')