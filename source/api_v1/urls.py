from django.urls import include, path
from rest_framework import routers
from api_v1 import views
from api_v1.views import get_token_view
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'basket', views.BasketViewSet)

app_name = 'api_v1'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('get-token/', get_token_view, name='get_token'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]