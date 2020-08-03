from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect

from webapp.forms import ProductForm, ProductCategory
from webapp.models import Product


def index_view(request):

    data = Product.objects.all().order_by('name','category')
    category =  ProductCategory()
    return render(request, 'index.html', context={
        'products': data,
        'category': category
    })

def category_view(request,ct):

    data = Product.objects.all().filter(category=ct)
    category = ProductCategory()
    return render(request, 'index.html', context={
        'products': data,
        'category': category
    })


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {'product': product}
    return render(request, 'product_view.html', context)


def create_product(request):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'create.html', context={'form': form})
    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            article = Product.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                amount=form.cleaned_data['amount'],
                price=form.cleaned_data['price']
            )
            return redirect('index')
        else:
            return render(request, 'create.html', context={'form': form})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])

def product_update_view(request, pk):

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        form = ProductForm(initial={
            'name': product.name,
            'description': product.description,
            'category': product.category,
            'amount': product.amount,
            'price': product.price
        })
        return render(request, 'update.html', context={
            'form': form,
            'article': product
        })

    elif request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name'],
            product.description = form.cleaned_data['description'],
            product.category = form.cleaned_data['category'],
            product.amount = form.cleaned_data['amount'],
            product.price = form.cleaned_data['price'],
            product.save()
            return redirect('index')
        else:
            return render(request, 'update.html', context={
                'product': product,
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])



def delete_product(request, pk):
    article = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        return render(request, 'delete.html', context={'article': article})
    elif request.method == 'POST':
        article.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])