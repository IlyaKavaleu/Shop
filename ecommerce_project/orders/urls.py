from django.urls import path, include
from .views import OrderCreateView, SuccessTemplateView, CancelTemplateView, OrderListView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('', OrderListView.as_view(), name='orders_list'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order'),
    path('order_success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order_canceled/', CancelTemplateView.as_view(), name='order_canceled'),
]
