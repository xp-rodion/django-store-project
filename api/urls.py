from django.urls import include, path
from rest_framework import routers

from api.views import BasketModelViewSet, ProductModelViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'baskets', BasketModelViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),

]