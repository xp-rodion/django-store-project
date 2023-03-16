from django.urls import path

from products.views import *

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsAfterCategoriesListView.as_view(), name='category'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('category_products/<int:category_id>/page/<int:page>/', ProductsAfterCategoriesListView.as_view(), name='category_paginator'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_item_id>/', basket_remove, name='basket_remove'),
]