from rest_framework import fields, serializers

from products.models import BasketItem, Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'category')


class BasketSerializer(serializers.ModelSerializer):
    sum = fields.FloatField()
    product = ProductSerializer()
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = BasketItem
        fields = ('id', 'product', 'quantity', 'sum', 'created_timestamp', 'total_sum', 'total_quantity')
        read_only_fields = ('created_timestamp', )

    def get_total_sum(self, obj):
        return BasketItem.objects.filter(user__id=obj.user.id).total_sum()

    def get_total_quantity(self, obj):
        return BasketItem.objects.filter(user__id=obj.user.id).total_quantity()