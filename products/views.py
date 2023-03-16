from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import ProductMixin, TitleMixin
from products.models import BasketItem, Product


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(ProductMixin, ListView):
    template_name = 'products/products.html'
    title = 'Store - Каталог'


class ProductsAfterCategoriesListView(ProductMixin, ListView):
    template_name = 'products/products_category.html'
    title = 'Store - Каталог'

    def get_context_data(self, *, products=None, **kwargs):
        context = super(ProductsAfterCategoriesListView, self).get_context_data(products=None, **kwargs)
        context['category_id'] = self.kwargs.get('category_id')
        return context

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        queryset = super(ProductsAfterCategoriesListView, self).get_queryset()
        return queryset.filter(category_id=category_id)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    basket_item = BasketItem.objects.filter(user=request.user, product=product).first()

    if not basket_item:
         BasketItem.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket_item.quantity += 1
        basket_item.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_item_id):
    item = BasketItem.objects.get(id=basket_item_id)
    item.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])