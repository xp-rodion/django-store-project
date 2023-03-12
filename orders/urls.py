from django.urls import path
from orders.views import OrderCreateView, SuccessTemplateView, CanceledTemplateView, OrderListView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order-create'),
    path('order-success/', SuccessTemplateView.as_view(), name='order-success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order-canceled'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),

]