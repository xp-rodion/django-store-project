from django.db import models
from django.http import HttpResponse

from common.views import validate_quantity
from products.models import BasketItem, Product
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.TextField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order #{self.id}| {self.first_name} {self.last_name}'

    def save(self, update=False, force_insert=False, force_update=False, using=None,
             update_fields=None):
        baskets = BasketItem.objects.filter(user=self.initiator)
        if update is False:
            self.basket_history = {
                'purchased_items': [basket.de_json() for basket in baskets],
                'total_sum': float(baskets.total_sum()),
            }
        return super(Order, self).save(force_insert=False, force_update=False, using=None,
                                       update_fields=None)

    def update_after_payment(self):
        baskets = BasketItem.objects.filter(user=self.initiator)
        for item in baskets:
            if not validate_quantity(item, operation=True):
                return HttpResponse(f'Error: Товар {item.product} закончился.')
        self.status = self.PAID
        baskets.delete()
        self.save(update=True)
