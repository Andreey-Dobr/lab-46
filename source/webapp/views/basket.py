from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DeleteView, UpdateView, CreateView

from webapp.forms import BasketForm, OrderForms
from webapp.models import Basket, Product





class BasketListView(ListView):
    template_name = 'basket/basketlist.html'
    context_object_name = 'baskets'
    model = Basket
    form_class = OrderForms



class AddBasket(CreateView):
    template_name = 'basket/add_basket.html'
    form_class = BasketForm
    model = Basket

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        basket = form.save(commit=False)
        basket.poll = product
        basket.save()

        return redirect('index')



class Basket_Delete(DeleteView):
    model = Basket

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('basket')
