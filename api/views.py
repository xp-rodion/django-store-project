from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from products.models import Product, BasketItem
from products.serializers import ProductSerializer, BasketSerializer


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action != 'list':
            self.permission_classes = IsAdminUser,
        return super(ProductModelViewSet, self).get_permissions()


class BasketModelViewSet(ModelViewSet):
    queryset = BasketItem.objects.all()
    serializer_class = BasketSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        queryset = super(BasketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)