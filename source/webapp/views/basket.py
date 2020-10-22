from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView, CreateView

from webapp.forms import BasketForm, OrderForms
from webapp.models import Basket, Product, Order, OrderProduct


class BasketListView(ListView):
    template_name = 'basket/basketlist.html'
    context_object_name = 'baskets'

    def get_queryset(self):
        return Basket.get_with_product().filter(pk__in=self.get_cart_ids())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['cart_total'] = Basket.get_cart_total(ids=self.get_cart_ids())
        context['form'] = OrderForms()
        return context

    def get_cart_ids(self):
        cart_ids = self.request.session.get('cart_ids', [])
        print(cart_ids)
        return self.request.session.get('cart_ids', [])



#class AddBasket(CreateView):
#    template_name = 'basket/add_basket.html'
#    form_class = BasketForm
#    model = Basket
#
#    def form_valid(self, form):
#        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
#        basket = form.save(commit=False)
#        basket.poll = product
#        basket.save()

#        return redirect('index')

class AddBasket(CreateView):
    model = Basket
    form_class = BasketForm

    def post(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # qty = 1
        # бонус
        count = form.cleaned_data.get('qty', 1)

        try:
            cart_product = Basket.objects.get(product=self.product, pk__in=self.get_cart_ids())
            cart_product.qty += count
            if cart_product.count <= self.product.amount:
                cart_product.save()
        except Basket.DoesNotExist:
            if count <= self.product.amount:
                cart_product = Basket.objects.create(product=self.product, count=count)
                self.save_to_session(cart_product)

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return redirect(self.get_success_url())

    def get_success_url(self):
        # бонус
        next = self.request.GET.get('next')
        if next:
            return next
        return reverse('webapp:index')

    def get_cart_ids(self):
        return self.request.session.get('cart_ids', [])

    def save_to_session(self, cart_product):
        cart_ids = self.request.session.get('cart_ids', [])
        if cart_product.pk not in cart_ids:
            cart_ids.append(cart_product.pk)
        self.request.session['cart_ids'] = cart_ids



#class Basket_Delete(DeleteView):
#    model = Basket
#
#    def get(self, request, *args, **kwargs):
#        return self.delete(request, *args, **kwargs)
#
#    def get_success_url(self):
#        return reverse('basket')

class Basket_Delete(DeleteView):
    model = Basket
    success_url = reverse_lazy('basket/basketlist.html')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.delete_from_session()
        self.object.delete()
        return redirect(success_url)

    def delete_from_session(self):
        cart_ids = self.request.session.get('cart_ids', [])
        cart_ids.remove(self.object.pk)
        self.request.session['cart_ids'] = cart_ids

    # удаление без подтверждения
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class BasketDeleteOneView(Basket_Delete):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.qty -= 1
        if self.object.qty < 1:
            self.delete_from_session()
            self.object.delete()
        else:
            self.object.save()

        return redirect(success_url)





class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForms
    success_url = reverse_lazy('webapp:index')


    def form_valid(self, form):
        response = super().form_valid(form)
        order = self.object
        # оптимально:
        # цикл сам ничего не создаёт, не обновляет, не удаляет
        # цикл работает только с объектами в памяти
        # и заполняет два списка: products и order_products
        cart_products = Basket.objects.all()
        products = []
        order_products = []
        for item in cart_products:
            product = item.product
            qty = item.qty
            product.amount -= qty
            products.append(product)
            order_product = OrderProduct(order=order, product=product, qty=qty)
            order_products.append(order_product)
        OrderProduct.objects.bulk_create(order_products)

        Product.objects.bulk_update(products, ('amount',))
        cart_products.delete()
        return response

    def form_invalid(self, form):
        return redirect('basket/basketlist.html')
