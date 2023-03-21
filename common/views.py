from django.http import HttpResponse

from products.models import Product, ProductCategory


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class ProductMixin(TitleMixin):
    model = Product
    paginate_by = 1
    context_object_name = 'products'

    def get_context_data(self, *, products=None, **kwargs):
        context = super(ProductMixin, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


def validate_quantity(item, operation=False):
    product = Product.objects.get(id=item.product_id)
    if operation:
        product.quantity -= item.quantity
        product.save()
    return True if product.quantity < 1 else False
