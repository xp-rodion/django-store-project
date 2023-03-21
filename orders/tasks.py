from celery import shared_task

from orders.models import EmailOrder, Order


@shared_task
def send_information_order(order_id):
    order = Order.objects.get(id=order_id)
    record = EmailOrder.objects.create(order=order)
    record.send_order_information()