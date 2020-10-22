from rest_framework import serializers
from webapp.models import Product, Basket


class ProductSerializer(serializers.ModelSerializer):

   # tags = serializers.SlugRelatedField(slug_field='name', read_only=True)
   # author = serializers.SlugField(read_only=True)

    class Meta:
        model = Product
        exclude = ''

class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        exclude = ''