"""Product URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from webapp.views import \
    ProductListView, ProductView, ProjectCreate, Product_Update_View, Delete_Product, AddBasket
from webapp.views.basket import BasketListView, Basket_Delete

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', ProductListView.as_view(), name='index'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_view'),
    path('product/add/', ProjectCreate.as_view(), name='create_product'),
    path('product/<int:pk>/edit/', Product_Update_View.as_view(), name='update'),
    path('product/<int:pk>/del/', Delete_Product.as_view(), name='del'),


    path('basket/', BasketListView.as_view(), name='basket'),
    path('product/<int:pk>/basket/', AddBasket.as_view(), name='basket_add'),
    path('<int:pk>/basket/', Basket_Delete.as_view(), name='basket_delete'),

]


