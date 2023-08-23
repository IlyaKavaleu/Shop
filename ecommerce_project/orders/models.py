from urllib import request

from django.db import models
from shop.models import User

from shop.models import Cart

from shop.views import _cart_id

from shop.models import CartItem


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Created'),
        (PAID, 'Paid'),
        (ON_WAY, 'On way'),
        (DELIVERED, 'Delivered'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    cart_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)  # WYBORKA
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order #{self.id}. {self.first_name} {self.last_name}'

    def update_after_payment(self):
        cart = Cart.objects.filter(cart_id=_cart_id(request), user=self.initiator)
        carts = CartItem.objects.filter(cart=cart)
        self.status = self.PAID
        self.cart_history = {
            'purchased_items': [cart.de_json() for cart in carts],
            'total_sum': float(carts.sum()),
        }
        cart.delete()
        self.save()
