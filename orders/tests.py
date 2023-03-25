from django.test import TestCase

from common.views import validate_quantity
from products.models import BasketItem, Product, ProductCategory
from users.models import User


class ProductQualityTestCase(TestCase):
    def test_work_quantity(self):
        test_user = User.objects.create(username='test', email='test@mail.ru')
        test_category = ProductCategory.objects.create(name='Обувь')
        test_quantity_1 = 10
        test_quantity_2 = 13
        test_product_1 = Product.objects.create(name='Кроссовки', description='Удобные', price=3200,
                                                quantity=test_quantity_1, image=None, category=test_category)
        test_product_2 = Product.objects.create(name='Кожаные ботинки', description='Красивые', price=6400,
                                                quantity=test_quantity_2, image=None, category=test_category)
        test_quantity_basket_item_1 = 2
        test_quantity_basket_item_2 = 3
        test_basket_item_1 = BasketItem.objects.create(user=test_user, product=test_product_1,
                                                       quantity=test_quantity_basket_item_1)
        test_basket_item_2 = BasketItem.objects.create(user=test_user, product=test_product_2,
                                                       quantity=test_quantity_basket_item_2)
        validate_quantity(test_basket_item_1, operation=True)
        validate_quantity(test_basket_item_2, operation=True)
        self.assertEqual(test_quantity_1 - test_quantity_basket_item_1, test_product_1.quantity)
        self.assertEqual(test_quantity_2 - test_quantity_basket_item_2, test_product_2.quantity)
