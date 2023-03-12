from django.urls import path, include

from api.views import ProductModelViewSet, BasketModelViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'baskets', BasketModelViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),

]