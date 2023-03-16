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