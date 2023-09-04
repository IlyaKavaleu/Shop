from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from orders.forms import OrderForm
import stripe
from shop.models import Cart
# from ecommerce_app import settings
from django.views.generic.base import TemplateView
from stripe.error import SignatureVerificationError
from shop.models import CartItem
from .models import Order
from ecommerce_app import settings

stripe.api_key = 'sk_test_51Nlu7CKqkSR9oZm7UZC1nWzgbjhyjp0jqYYnOdNPC7O1sLFEBLC5PSRTUizX6ILl85ouZ63BBD5vHCfxKg95dQcj008XVt3UlC'
stripe_webhook_secret = 'whsec_e1088eafaba7ac245ac80eec91eb7ac32e002cd3d3e5ef9355b65c51f9f6f9c8'


class SuccessTemplateView(TemplateView):
    template_name = 'orders/order_success.html'
    title = 'Success'


class CancelTemplateView(TemplateView):
    template_name = 'orders/order_canceled.html'
    title = 'Canceled'


class OrderListView(ListView):
    template_name = 'orders/orders.html'
    title = 'Orders'
    queryset = Order.objects.all()
    ordering = '-created'

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - Order #{self.object.id}'
        return context


class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Order'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        cart = Cart.objects.get(user=request.user)
        carts = CartItem.objects.filter(cart=cart)

        line_items = []
        for cart_item in carts:
            line_items.append({
                'price_data': {
                    'currency': 'usd',  # Замените на вашу валюту
                    'product_data': {
                        'name': cart_item.product.name,  # Замените на соответствующее поле в модели Product
                    },
                    'unit_amount': int(cart_item.product.price * 100),  # Преобразуйте в центы
                },
                'quantity': cart_item.quantity,
            })

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, HTTPStatus.SEE_OTHER)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = event['data']['object']
        # Fulfill the purchase...
        fulfill_order(session)
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
