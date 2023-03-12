from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import BasketItem, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(TitleMixin, ListView):
    template_name = 'products/products.html'
    model = Product
    paginate_by = 2
    title = 'Store - Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        print(queryset)
        return queryset.filter(category_id=category_id) if category_id else queryset


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