from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from webapp.models import Product, Basket
from rest_framework.decorators import action
from api_v1.serializers import ProductSerializer, BasketSerializer
from rest_framework.permissions import IsAuthenticated



@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')

#class ProductViewSet(viewsets.ModelViewSet):
#    queryset = Product.objects.all()
#    serializer_class = ProductSerializer

class ProductViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

    def list(self, request):
        objects = Product.objects.all()
        slr = ProductSerializer(objects, many=True, context={'request': request})
        return Response(slr.data)



    def create(self, request):

        slr = ProductSerializer(data=request.data, context={'request': request})
        if slr.is_valid():
            product = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def retrieve(self, request, pk=None):
        article = get_object_or_404(Product, pk=pk)
        slr = ProductSerializer(article, context={'request': request})
        return Response(slr.data)

    def update(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        slr = ProductSerializer(data=request.data, instance=product, context={'request': request})
        if slr.is_valid():
            product = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def destroy(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({'pk': pk})


class BasketViewSet(ViewSet):
    queryset = Basket.objects.all()

    def list(self, request):
        objects = Basket.objects.all()
        slr = BasketSerializer(objects, many=True, context={'request': request})
        return Response(slr.data)

    def create(self, request):
        slr = BasketSerializer(data=request.data, context={'request': request})
        if slr.is_valid():
            basket = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)




