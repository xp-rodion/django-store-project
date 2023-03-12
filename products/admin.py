from django.contrib import admin

from products.models import BasketItem, Product, ProductCategory

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'category', 'image')
    readonly_fields = ('description', )
    search_fields = ('name', )
    ordering = ('name', )


class BasketAdmin(admin.TabularInline):
    model = BasketItem
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp', )
    extra = 0
