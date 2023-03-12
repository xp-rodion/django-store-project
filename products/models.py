import stripe

from django.db import models
from django.conf import settings
from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=256)
    price = models.DecimalField(max_digits=6, decimal_places=1)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.stripe_product_price_id:
            self.stripe_product_price_id = (self.create_stripe_product_price()).get('id')
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product.get('id'),
            unit_amount=round(self.price * 100),
            currency='rub'
        )
        return stripe_product_price

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'


class BasketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(item.sum() for item in self)

    def total_quantity(self):
        return sum(item.quantity for item in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class BasketItem(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Элемент корзины пользователя {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item
