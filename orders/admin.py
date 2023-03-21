from django.contrib import admin

from orders.models import EmailOrder, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    fields = ('id', 'created',
              ('first_name', 'last_name'),
              ('email', 'address'),
              'basket_history', 'status', 'initiator')
    readonly_fields = ('id', 'created', )


@admin.register(EmailOrder)
class EmailOrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created')
    fields = ('id', 'order', 'created')
    readonly_fields = ('id', 'created')

