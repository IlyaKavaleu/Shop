from django.urls import path, include
from .views import OrderCreateView, SuccessTemplateView, CancelTemplateView

app_name = 'orders'

urlpatterns = [
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order_success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order_canceled/', CancelTemplateView.as_view(), name='order_canceled'),
]
